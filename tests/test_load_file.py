import os
from unittest.mock import MagicMock, patch

from pydaconf import PydaConf
from pydaconf.utils.file import load_config_file
from pydantic import BaseModel


class Config(BaseModel):
    name: str

def test_provider_json() -> None:
    provider = PydaConf[Config]()
    provider.from_file(os.path.join('tests', 'resources', 'config.json'))
    assert provider.config.name == 'Test'

def test_provider_yaml() -> None:
    provider = PydaConf[Config]()
    provider.from_file(os.path.join('tests', 'resources', 'config.yaml'))
    assert provider.config.name == 'Test'

def test_provider_toml() -> None:
    provider = PydaConf[Config]()
    provider.from_file(os.path.join('tests', 'resources', 'config.toml'))
    assert provider.config.name == 'Test'

def test_load_from_url() -> None:
    mock_response = MagicMock()
    mock_response.text = """name: Test"""
    
    with patch("requests.get", return_value=mock_response):
        provider = PydaConf[Config]()
        provider.from_url('http://dummy.url/config.yaml')
        assert provider.config.name == 'Test'

def test_yaml_content_guess() -> None:
    config = load_config_file(os.path.join('tests', 'resources', 'config.conf-yaml'))
    assert config['name'] == 'Test'

def test_json_content_guess() -> None:
    config = load_config_file(os.path.join('tests', 'resources', 'config.conf-json'))
    assert config['name'] == 'Test'

def test_toml_content_guess() -> None:
    config = load_config_file(os.path.join('tests', 'resources', 'config.conf-toml'))
    assert config['name'] == 'Test'