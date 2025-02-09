import pytest

from pydaconf import PydaConf
from pydaconf.utils.exceptions import InterpolationException
from pydantic import BaseModel


class Connection(BaseModel):
    protocol: str
    port: int
    host: str

class Config(BaseModel):
    connection: Connection
    url: str


def test_interpolation_with_spaces()  -> None:
    config = {
        "connection": {
            "protocol": "https",
            "host": "example.com",
            "port": 443

        },
        "url": "{{ connection.protocol }}://{{ connection.host }}:{{ connection.port }}"
    }

    provider = PydaConf[Config](Config)
    provider.from_dict(config)
    assert provider.config.url == "https://example.com:443"

def test_interpolation_without_spaces()  -> None:
    config = {
        "connection": {
            "protocol": "https",
            "host": "example.com",
            "port": 443

        },
        "url": "{{connection.protocol}}://{{connection.host}}:{{connection.port}}"
    }

    conf_provider: PydaConf[Config] = PydaConf[Config](Config)
    conf_provider.from_dict(config)
    assert conf_provider.config.url == "https://example.com:443"

def test_interpolation_raise_exception() -> None:
    config = {
        "connection": {
            "protocol": "https",
            "host": "example.com",
            "port": 443

        },
        # connection.schema is not defined
        "url": "{{connection.schema}}://{{connection.host}}:{{connection.port}}"
    }

    conf_provider = PydaConf[Config](Config)
    with pytest.raises(InterpolationException):
        conf_provider.from_dict(config)
        assert conf_provider.config