import logging
import re
import threading
from collections.abc import Callable
from functools import partial
from typing import Generic, TypeAlias, TypeVar, get_args

from pydaconf.plugins.base import PluginBase
from pydaconf.utils.exceptions import ProviderException
from pydaconf.utils.file import load_config_file, load_from_url
from pydaconf.utils.interpolation import (
    has_interpolation_template,
    interpolate_template,
)
from pydaconf.utils.plugins import load_builtin_plugins, load_dynamic_plugins
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)
ConfigValueType: TypeAlias = list | dict | str | int | bool | None

class PydaConf(Generic[T]):

    def __init__(self) -> None:
        self._raw_config: dict | None = None
        self._config: T | None = None
        self._plugins: dict[str, PluginBase] = {}
        self._update_subscribers: dict[str, list[Callable[[str, str], None]]] = {}
        self._update_lock = threading.Lock()
        self.logger = logging.getLogger(__name__)

    def from_file(self, file_path: str) -> None:
        self._load_plugins()
        self._raw_config = load_config_file(file_path)

    def from_url(self, url: str) -> None:
        self._load_plugins()
        self._raw_config = load_from_url(url)

    def from_dict(self, dict_data: dict) -> None:
        self._load_plugins()
        self._raw_config = dict_data

    @property
    def config(self) -> T:
        if self._raw_config is None:
            raise ProviderException("""PydaConf is not initialized. 
                                    You need to run on of these methods first from_file('file_path'), from_dict(dict_data) or from_url(url).""")

        if self._config is None:
            config_copy = self._raw_config.copy()
            self.logger.debug("Inject credentials to the config")
            self._inject_secrets(config_copy)
            self.logger.debug("Interpolate values")
            self._interpolate_templates(config_copy, config_copy)

            try:
                self.logger.debug("Build config object")
                config: T = self._get_generic_type()(**config_copy)
                self._config = config
            except ValidationError as e:
                raise ProviderException('Configuration file validation failed with errors', e.errors()) from e

        return self._config

    def register_plugin(self, plugin_class: type[PluginBase]) -> None:
        """ Manually register plugin """
        self._plugins[str(plugin_class.PREFIX)] = plugin_class()

    def on_update(self, key_pattern: str, callback: Callable[[str, str], None]) -> None:
        """Subscribe to an update events of specific pattern."""
        self._update_subscribers.setdefault(key_pattern, [])
        self._update_subscribers[key_pattern].append(callback)

    def _get_generic_type(self) -> type[T]:
        """Return the type of generic T """

        # This is a bit hacky method since __orig_class__ is not well documented and could be changed in future...
        orig_class = getattr(self, '__orig_class__', None)
        if orig_class is None:
            raise ProviderException('PydaConf must be defined as generic Config[MyPydanticType]()')

        generic_type: type[T] | None = next(iter(get_args(orig_class)), None)
        if generic_type is None or not issubclass(generic_type, BaseModel):
            raise ProviderException('Generic type must inherit pydantic BaseModel class Config[MyPydanticType]()')

        return generic_type

    def _load_plugins(self) -> None:
        self._load_builtin_plugins()
        self._load_dynamic_plugins()
        
    def _load_builtin_plugins(self) -> None:
        for plugin in load_builtin_plugins():
            self._plugins[plugin.PREFIX] = plugin
    
    def _load_dynamic_plugins(self) -> None:
        for plugin in load_dynamic_plugins():
            self._plugins[plugin.PREFIX] = plugin

    def _interpolate_templates(self, node: ConfigValueType, config_data: dict) -> None:
        if isinstance(node, list):
            for index, element in enumerate(node):
                if type(element) is str:
                    node[index] = interpolate_template(element, config_data)
                else:
                    self._interpolate_templates(element, config_data)

        elif isinstance(node, dict):
            for key, element in node.items():
                if isinstance(element, dict) or isinstance(element, list):
                    self._interpolate_templates(element, config_data)
                
                elif isinstance(element, str):
                    if has_interpolation_template(element):
                        node[key] = interpolate_template(element, config_data)


    def _match_and_execute_plugin(self, element: str, key: str) -> str:
        match_prefix = re.match(r'(?P<PLUGIN_PREFIX>[^:]+):///(?P<VALUE>[^\s]+)', element)
        if match_prefix:
            plugin_prefix = match_prefix.groupdict()['PLUGIN_PREFIX']
            value = match_prefix.groupdict()['VALUE']
            plugin = self._plugins.get(plugin_prefix.upper())
            if plugin is None:
                raise ProviderException(f"Plugin with prefix '{plugin_prefix}' is not registered")
            return plugin._execute_plugin(value, partial(self._on_update, key))
        else:
            return element

    def _inject_secrets(self, node: ConfigValueType, key_path: str="") -> None:
        if isinstance(node, list):
            for index, element in enumerate(node):
                if type(element) is str:
                   node[index] = self._match_and_execute_plugin(element, f"{key_path}[{index}]")
                else:
                    self._inject_secrets(element, key_path=f"{key_path}[{index}]")

        elif isinstance(node, dict):
            for key, element in node.items():
                if isinstance(element, dict) or isinstance(element, list):
                    self._inject_secrets(element, key_path=f"{key_path}.{key}")

                elif isinstance(element, str):
                    node[key] = self._match_and_execute_plugin(element, f"{key_path}.{key}")

    def _update_config(self, key: str, value: str) -> None:
        """ Update the configuration base on key and value """

        # Unfortunately, I could find a better way to do this directly on the pyndatic model
        # TODO: Research a better option with setattr and getattr
        if self._config is None:
            raise ProviderException('PydaConf is not initialized, or you call on_update callback in the plugin run.')

        config_model = self._config.model_dump()
        current = config_model
        keys = re.split(r'\.(?![^\[]*\])', key.lstrip('.'))  # Split while ignoring dots inside brackets

        for key in keys[:-1]:  # Traverse until the second last key
            match = re.match(r'(\w+)\[(\d+)\]', key)  # Match list indexing pattern, e.g., users[0]

            if match:
                key, index = match.groups()
                index = int(index)
                current = current[key][index]  # Move to the specific index
            else:
                current = current[key]  # Move deeper

        # Process the last key
        final_key = keys[-1]
        match = re.match(r'(\w+)\[(\d+)\]', final_key)

        if match:
            key, index = match.groups()
            index = int(index)
            current[key][index] = value  # Update value at the index
        else:
            current[final_key] = value  # Update the final key

        self._config = self._get_generic_type()(**config_model)


    def _on_update(self, key: str, value: str) -> None:
        """ Update the configuration and notify all subscribers registered for specific key pattern """

        # We use thread lock to protection against race conditions when threads access shared objects.
        with self._update_lock:
            self._update_config(key, value)

        for key_patters, subscribers in self._update_subscribers.items():
            if re.match(key_patters, key):
                for subscriber in subscribers:
                    subscriber(key, value)


    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.config.model_dump()})'
