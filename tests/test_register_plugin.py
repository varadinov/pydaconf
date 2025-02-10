from collections.abc import Callable

from pydaconf import PydaConf
from pydaconf.plugins.base import PluginBase
from pydantic import BaseModel


class Config(BaseModel):
    name: str
    secret: str

class TestPlugin(PluginBase):

    PREFIX = "TEST"

    def run(self, value: str, on_update_callback: Callable) -> str:
        return value
    

def test_register_plugin() -> None:
    config = {
       "name": 'test',
       "secret": "TEST:///TEST"
    }
    provider = PydaConf[Config]()
    provider.from_dict(config)
    provider.register_plugin(TestPlugin)
    assert provider.config.secret == 'TEST'