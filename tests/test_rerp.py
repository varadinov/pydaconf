from pydaconf import PydaConf
from pydantic import BaseModel


class Config(BaseModel):
    username: str
    password: str

def test_repr() -> None:
    config = {
        'username': 'test',
        'password': 'test'
    }

    provider = PydaConf[Config](Config)
    provider.from_dict(config)
    assert str(provider) == "PydaConf({'username': 'test', 'password': 'test'})"