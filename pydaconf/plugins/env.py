import os
from collections.abc import Callable

from dotenv import load_dotenv

from pydaconf.plugins.base import PluginBase

# TODO: Remove the cache since the provider implements its own cache

class EnvPlugin(PluginBase):
    """Environment variables plugin. Loads environment variable based on prefix ENV:///"""

    PREFIX='ENV'

    def __init__(self) -> None:
        self.cache: dict[str, str] = {}

    def run(self, value: str, on_update_callback: Callable[[str], None]) -> str:
        load_dotenv()
        if value not in self.cache:
            env_var = os.environ.get(value)
            if not env_var:
                raise Exception(f"Secret cannot be loaded for '{value}'. Environment '{value}' is empty.")
            
            self.cache[value] = env_var
    
        return self.cache[value]
