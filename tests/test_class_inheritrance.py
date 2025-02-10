from pydaconf import PydaConf
from pydantic import BaseModel


class BaseConfig(BaseModel):
    username: str

class SecureConfig(BaseConfig):
    password: str

def test_class_inheritance() -> None:
    config = {
        'username': 'test',
        'password': 'test'
    }

    provider = PydaConf[SecureConfig]()
    provider.from_dict(config)
    assert str(provider) == "PydaConf({'username': 'test', 'password': 'test'})"