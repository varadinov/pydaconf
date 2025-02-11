from collections.abc import Callable
from unittest.mock import MagicMock, patch

from pydaconf import PydaConf
from pydaconf.plugins.base import PluginBase
from pydaconf.utils.plugins import load_builtin_plugins, load_dynamic_plugins
from pydantic import BaseModel


class InvalidPlugin:
    pass

class DummyPlugin(PluginBase):

    PREFIX = 'DUMMY'

    def run(self, value: str, on_update_callback: Callable[[str], None]) -> str:
        return value


def test_load_builtin_plugins() -> None:
    plugins = list(load_builtin_plugins())
    assert len(plugins) > 0


def test_load_dynamic_plugins() -> None:
    with patch("importlib.metadata.entry_points") as mock_entry_points:
        dummy_plugin = MagicMock()
        dummy_plugin.load.return_value = DummyPlugin

        mock_entry_points.return_value = [dummy_plugin]

        # Execute the function under test
        plugins = list(load_dynamic_plugins())

        # Assertions
        assert len(plugins) == 1
        assert isinstance(plugins[0], DummyPlugin)
        assert plugins[0].run('test', lambda d: None) == 'test'

def test_skip_invalid_plugin() -> None:
    with patch("importlib.metadata.entry_points") as mock_entry_points:
        invalid_plugin = MagicMock()
        invalid_plugin.load.return_value = InvalidPlugin

        mock_entry_points.return_value = [invalid_plugin]

        # Execute the function under test
        plugins = list(load_dynamic_plugins())

        # Assertions
        assert len(plugins) == 0


def test_provider_load_dynamic_plugins() -> None:
    class Config(BaseModel):
        test: str

    with patch("importlib.metadata.entry_points") as mock_entry_points:
        dummy_plugin = MagicMock()
        dummy_plugin.load.return_value = DummyPlugin

        mock_entry_points.return_value = [dummy_plugin]

        provider = PydaConf[Config]()
        provider.from_dict({'test': 'test'})
        _ = provider.config
        assert isinstance(provider._plugins['DUMMY'], DummyPlugin)
