import os
from collections.abc import Callable

from pydaconf.plugins.base import PluginBase
from pydaconf.utils.exceptions import ProviderException


class SealedPlugin(PluginBase):
    """Load sealed secret. Load/Decrypt sealed secret as variable based on prefix SEALED:///"""

    PREFIX='SEALED'

    def __init__(self) -> None:
        self.cache: dict[str, str] = {}

    def run(self, value: str, on_update_callback: Callable[[str], None]) -> str:
        if value not in self.cache:
            key = os.environ.get('PYDACONF_SEALED_KEY')
            if key is None:
                raise ProviderException(f"PYDACONF_SEALED_KEY environment variable is required to decrypt '{value}'")
            
            try:
                from cryptography.fernet import Fernet
                encryption_provider = Fernet(key)
            except ImportError as e:
                raise ImportError('Cryptography is not installed, run `pip install pydaconf[cryptography]`') from e

            content = encryption_provider.decrypt(value)

            self.cache[value] = content.decode()
    
        return self.cache[value]

