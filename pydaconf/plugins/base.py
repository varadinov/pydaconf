from abc import ABC, abstractmethod
from collections.abc import Callable

from pydaconf.utils.exceptions import PluginException


class PluginBase(ABC):
    """Abstract Base Class for plugins."""

    def _execute_plugin(self, value: str, on_update_callback: Callable[[str], None]) -> str:
        """This method is intended to be called only from PyDaConf provider"""
        try:
            return self.run(value, on_update_callback)
        except Exception as e:
            raise PluginException(
                f"Plugin '{self.__class__.__name__}' failed to get data for value '{value}'. Error: {str(e)}") from e

    @property
    @abstractmethod
    def PREFIX(self) -> str:
        raise NotImplementedError


    @abstractmethod
    def run(self, value: str, on_update_callback: Callable[[str], None]) -> str:
        raise NotImplementedError