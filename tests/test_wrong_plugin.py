import pytest

from pydaconf import ProviderException, PydaConf
from pydantic import BaseModel


class Config(BaseModel):
    name: str
    secret: str

def test_env_plugin() -> None:
    config = {
        "name": "Test",
        "secret": "WRONG:///TEST"
    }
    conf_provider = PydaConf[Config]()
    with pytest.raises(ProviderException, match="Plugin with prefix 'WRONG' is not registered"):
        conf_provider.from_dict(config)
        _ = conf_provider.config