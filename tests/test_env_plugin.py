from unittest.mock import MagicMock, patch

from pydaconf import PydaConf
from pydantic import BaseModel


class Config(BaseModel):
    name: str
    secret: str

def test_env_plugin() -> None:
    config = {
        "name": "Test",
        "secret": "ENV:///TEST"
    }
    conf_provider = PydaConf[Config]()
    with patch("os.environ") as environ:
        environ.get = MagicMock(return_value = 'TEST')

        conf_provider.from_dict(config)
        assert conf_provider.config.secret == 'TEST'