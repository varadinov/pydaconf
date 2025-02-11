import pytest

from pydaconf import PydaConf
from pydaconf.utils.exceptions import ProviderException
from pydantic import BaseModel


class Config(BaseModel):
    username: str
    password: str

def test_not_initialized() -> None:
    provider = PydaConf[Config]()
    with pytest.raises(ProviderException):
        assert provider.config


def test_second_initialized() -> None:
    provider = PydaConf[Config]()
    provider.from_dict({'username': 'test', 'password': 'pass'})
    assert provider.config.username == 'test'
    assert provider.config.password == 'pass'
