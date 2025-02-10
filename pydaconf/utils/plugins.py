import importlib
import importlib.metadata
import inspect
import os
import pkgutil
from collections.abc import Iterator

import pydaconf.plugins
from pydaconf.plugins.base import PluginBase


def load_builtin_plugins() -> Iterator[PluginBase]:
    for _, module_name, _ in pkgutil.iter_modules([str(f"{os.path.dirname(pydaconf.plugins.base.__file__)}")]):
        full_module_name = f"{pydaconf.plugins.__name__}.{module_name}"
        module = importlib.import_module(full_module_name) 

        # Inspect module and find classes that subclass PluginBase
        for _, plugin_class in inspect.getmembers(module, inspect.isclass):
            if issubclass(plugin_class, PluginBase) and plugin_class is not PluginBase:
                yield plugin_class()

def load_dynamic_plugins() -> Iterator[PluginBase]:
    for entry_point in importlib.metadata.entry_points(group='pydaconf.plugins'):
        plugin_class = entry_point.load()
        if issubclass(plugin_class, PluginBase):
            yield plugin_class()