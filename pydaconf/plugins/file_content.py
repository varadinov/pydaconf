from collections.abc import Callable

from pydaconf.plugins.base import PluginBase


class FileContentPlugin(PluginBase):
    """Load file content as variable plugin. Loads file content as variable based on prefix FILE_CONTENT:///"""

    PREFIX='FILE_CONTENT'

    def __init__(self) -> None:
        self.cache: dict[str, str]= {}

    def run(self, value: str, on_update_callback: Callable[[str], None]) -> str:
        if value not in self.cache:
            try:
                with open(value) as file:
                    content = file.read()

            except Exception as e:
                raise Exception(f"Secret cannot be loaded from file '{value}'. Error", e)

            self.cache[value] = content
    
        return self.cache[value]
