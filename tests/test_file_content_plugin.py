from pydaconf import PydaConf
from pydantic import BaseModel


class Config(BaseModel):
    name: str
    secret: int

def test_file_content_load() -> None:
    config = {
       "name": "Test",
       "secret": "FILE_CONTENT:///tests/resources/file_content_plugin.txt"
    }
    provider = PydaConf[Config]()
    provider.from_dict(config)
    assert provider.config.secret == 24