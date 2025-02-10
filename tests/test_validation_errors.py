import pytest

from pydaconf import PydaConf
from pydaconf.utils.exceptions import ProviderException
from pydantic import BaseModel


class Config(BaseModel):
    username: str
    password: str

def test_validation_errors() -> None:
    provider = PydaConf[Config]()
    with pytest.raises(ProviderException):
        provider.from_dict({'username': "test"})
        _ = provider.config
