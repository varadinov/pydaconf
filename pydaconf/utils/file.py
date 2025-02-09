import os
import sys

from pydaconf.utils.exceptions import UnknownFormat


def guess_content_format(content: str) -> str | None:
    """Guess file format based on the first line. This is much faster for big config files than using the parsers."""

    first_line = next(iter(content.splitlines()), None)
    if first_line is None:
        raise UnknownFormat("Config file first line is empty. Unable to identify the format")

    if first_line.startswith("{") or (first_line.startswith("[") and "]" in first_line and "=" not in first_line):
        return 'json'

    elif ":" in first_line and not first_line.startswith("["):
        return 'yaml'

    elif first_line.startswith("[") and "=" not in first_line:
        return 'toml'

    elif "=" in first_line:
        return 'toml'

    else:
        return None

def load_yaml_content(content: str) -> dict:
    try:
        import yaml
    except ImportError as e:
        raise ImportError('PyYAML is not installed, run `pip install pydaconf[yaml]`') from e

    result: dict | None = yaml.load(content, Loader=yaml.FullLoader)
    if result is None:
        raise ValueError("Empty yaml content")

    return result
    

def load_json_content(content: str) -> dict:
    import json
    result: dict | None = json.loads(content)
    if result is None:
        raise ValueError("Empty Json content")

    return result
    

def load_toml_content(content: str) -> dict:
    if sys.version_info < (3, 11):
        try:
            import tomli
            toml_module = tomli
        except ImportError as e:
            raise ImportError('Toml is not installed, run `pip install pydaconf[toml]`') from e
    else:
        import tomllib
        toml_module = tomllib
    
    return toml_module.loads(content)

def load_config_file(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file '{file_path}' doesn't exist")
    
    with open(file_path) as f:
        content = f.read()

    # Guess the file based on extension
    _, extension = os.path.splitext(file_path)
    if extension.lower() in {'.yaml', '.yml'}:
        return load_yaml_content(content)

    elif extension.lower() == '.json':
       return load_json_content(content)

    elif extension.lower() == '.toml':
        return load_toml_content(content)
    else:
        discovered_format = guess_content_format(content)
        if discovered_format == 'json':
            return load_json_content(content)
        elif discovered_format == 'yaml':
            return load_yaml_content(content)
        elif discovered_format == 'toml':
            return load_toml_content(content)
        else:
            raise UnknownFormat("Unknown config file format. Valid formats are json, yaml and toml.")

    
def load_from_url(url: str, headers: dict | None = None) -> dict:
    try:
        import requests
    except ImportError as e:
        raise ImportError('requests is not installed, run `pip install pydaconf[requests]`') from e
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    content = response.text
    discovered_format = guess_content_format(content)
    if discovered_format == 'json':
        return load_json_content(content)
    elif discovered_format == 'yaml':
        return load_yaml_content(content)
    elif discovered_format == 'toml':
        return load_toml_content(content)
    else:
        raise UnknownFormat("Unknown config file format")

    