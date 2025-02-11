import threading
import time
from collections.abc import Callable
from unittest.mock import Mock, call

import pytest

from pydaconf import ProviderException, PydaConf
from pydaconf.plugins.base import PluginBase
from pydantic import BaseModel


class ConnectionConfig(BaseModel):
    password: str

class User(BaseModel):
    username: str
    password: str

class Config(BaseModel):
    connection: ConnectionConfig
    users: list[User]
    developer: list[str]

class TestUpdatePlugin(PluginBase):
    """Test plugin"""

    PREFIX='ONUPDATE'

    def _run_on_update_in_thread(self, on_update_callback: Callable[[str], None]) -> None:
        def delayed_callback() -> None:
            time.sleep(0.2)
            on_update_callback('Update')

        threading.Thread(target=delayed_callback, daemon=True).start()

    def run(self, value: str, on_update_callback: Callable[[str], None]) -> str:
        self._run_on_update_in_thread(on_update_callback)
        return value


def test_on_update() -> None:
    mock_callback_connection_password = Mock()
    mock_callback_users_password = Mock()
    config = {
        "connection": {
            "password": "ONUPDATE:///Test1"  
        },
        "users": [
            { "username": "test", "password": "ONUPDATE:///Test2"},
            { "username": "test2", "password": "ONUPDATE:///Test3"},
        ],
        "developer": ["ONUPDATE:///Test4"]
    }
    provider = PydaConf[Config]()
    provider.register_plugin(TestUpdatePlugin)
    provider.from_dict(config)
    provider.on_update(r'.connection.password', mock_callback_connection_password)
    provider.on_update(r'.users.+', mock_callback_users_password)
    assert provider.config
    time.sleep(1)

    assert mock_callback_connection_password.call_count == 1
    expected_calls = [call('.connection.password', 'Update')]
    mock_callback_connection_password.assert_has_calls(expected_calls)


    assert mock_callback_users_password.call_count == 2
    expected_calls = [
        call('.users[0].password', 'Update'),
        call('.users[1].password', 'Update')]
    mock_callback_users_password.assert_has_calls(expected_calls, any_order=True)


def test_on_update_not_initialized() -> None:
    with pytest.raises(ProviderException):
        provider = PydaConf[Config]()
        provider._on_update('test', 'test')
