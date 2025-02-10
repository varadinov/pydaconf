import pytest

from pydaconf import ProviderException, PydaConf

config = {
    'username': 'test',
    'password': 'test'
}

def test_missing_base_model() -> None:
    with pytest.raises(ProviderException, match=r"PydaConf must be defined as generic Config\[MyPydanticType\]()"):
        provider = PydaConf() # type: ignore
        provider.from_dict(config)
        _ = provider.config

def test_wrong_type() -> None:
    class Config(dict):
        username: str
        password: str

    with pytest.raises(ProviderException, match=r"Generic type must inherit pydantic BaseModel class Config\[MyPydanticType\]()"):
        provider = PydaConf[Config]() # type: ignore
        provider.from_dict(config)
        _ = provider.config