from unittest.mock import patch

import pytest

from pydaconf import PydaConf
from pydaconf.utils.exceptions import PluginException
from pydantic import BaseModel


class Config(BaseModel):
    secret: str

def test_sealed_exception() -> None:
    config = {
        "secret": "SEALED:///gAAAAABnpRqHdho_dFB7iMs_Ufv5nu59LwqQfE3YCjaDTyg-YrYsEpK8bfvdKsdrj6kCxrAjezCGAdVM0FhzwyfYFIgqnquw8w=="
    }

    with patch('os.environ.get', return_value='WrongKey'):
        with pytest.raises(PluginException):
            provider: PydaConf[Config] = PydaConf[Config]()
            provider.from_dict(config)
            _ = provider.config

def test_sealed_load()  -> None:
    config = {
       "secret": "SEALED:///gAAAAABnpRqHdho_dFB7iMs_Ufv5nu59LwqQfE3YCjaDTyg-YrYsEpK8bfvdKsdrj6kCxrAjezCGAdVM0FhzwyfYFIgqnquw8w=="
    }

    with patch('os.environ.get', return_value='ky8Uv_xkl4WgvHjrrdffJDRV1D5G5pqBTBD0TNGtAi0='):
        provider: PydaConf[Config] = PydaConf[Config]()
        provider.from_dict(config)
        loaded_config = provider.config
        assert loaded_config.secret == 'Test Secret'