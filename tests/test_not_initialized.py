import pytest

from pydaconf import PydaConf
from pydaconf.utils.exceptions import ProviderException
from pydantic import BaseModel


class Config(BaseModel):
    username: str
    password: str

def test_not_initialized() -> None:
    provider = PydaConf[Config](Config)
    with pytest.raises(ProviderException):
        assert provider.config
