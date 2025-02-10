import pytest

from pydaconf import PydaConf
from pydaconf.utils.exceptions import InterpolationException
from pydantic import BaseModel


class Parameters(BaseModel):
    pool: bool
    replicas: dict[str, str]


class Connection(BaseModel):
    protocol: str
    port: int
    host: str
    parameters: Parameters


class Config(BaseModel):
    domain: str
    users: list[str]
    connection: Connection
    url: str


def test_interpolation_with_spaces()  -> None:
    config = {
        "domain": "example.com",
        "users": ["admin@{{ domain }}"],
        "connection": {
            "protocol": "https",
            "host": "example.com",
            "port": 443,
            "parameters": {
                "pool": True,
                "replicas": {
                    "primary": "primary@{{ domain }}",
                    "secondary": "secondary@{{ domain }}"
                }
            }

        },
        "url": "{{ connection.protocol }}://{{ connection.host }}:{{ connection.port }}"
    }

    provider = PydaConf[Config]()
    provider.from_dict(config)
    c = provider.config
    assert c.url == "https://example.com:443"
    assert c.connection.parameters.replicas['primary'] == "primary@example.com"
    assert c.connection.parameters.replicas['secondary'] == "secondary@example.com"
    assert c.users == ["admin@example.com"]

def test_interpolation_without_spaces()  -> None:
    config = {
        "domain": "example.com",
        "users": ["admin@{{domain}}"],
        "connection": {
            "protocol": "https",
            "host": "example.com",
            "port": 443,
            "parameters": {
                "pool": True,
                "replicas": {
                    "primary": "primary@{{domain}}",
                    "secondary": "secondary@{{domain}}"
                }
            }
        },
        "url": "{{connection.protocol}}://{{connection.host}}:{{connection.port}}"
    }

    provider: PydaConf[Config] = PydaConf[Config]()
    provider.from_dict(config)
    c = provider.config
    assert c.url == "https://example.com:443"
    assert c.connection.parameters.replicas['primary'] == "primary@example.com"
    assert c.connection.parameters.replicas['secondary'] == "secondary@example.com"
    assert c.users == ["admin@example.com"]

def test_interpolation_raise_exception() -> None:
    config = {
        "domain": "example.com",
        "users": ["admin@{{ domain }}"],
        "connection": {
            "protocol": "https",
            "host": "example.com",
            "port": 443,
            "parameters": {
                "pool": True,
                "replicas": {
                    "primary": "primary@{{ domain }}",
                    "secondary": "secondary@{{ domain }}"
                }
            }

        },
        # connection.schema is not defined
        "url": "{{connection.schema}}://{{connection.host}}:{{connection.port}}"
    }

    provider = PydaConf[Config]()
    with pytest.raises(InterpolationException):
        provider.from_dict(config)
        assert provider.config