# Developing and Packaging a PydaConf Plugin

PydaConf allows you to extend its functionality by developing and packaging custom plugins. Plugins enable dynamic injection of values from various sources such as external APIs, databases, or specialized secrets management systems.

## 1. Creating a Custom Plugin

A PydaConf plugin must inherit from `PluginBase` and define a `PREFIX` and `run` method.

### Example: Creating a local Custom Plugin

```python
from pydaconf.plugins.base import PluginBase
from collections.abc import Callable

class CustomPlugin(PluginBase):
    PREFIX = "CUSTOM"
    
    def run(self, value: str, on_update_callback: Callable[[str], None]) -> str:
        return f"Processed {value}"
```

## 2. Packaging the Plugin

To package the plugin as a standalone installable package, follow these steps:

### Create a `pyproject.toml` File

```toml
[build-system] # You can use your favoroite build backend system
requires = ["flit_core>=3.2,<4"]
build-backend = "flit_core.buildapi"

[project]
name = "pydaconf-plugins-custom"
version = "0.1.0"
description = "A custom plugin for PydaConf"
authors = [{ name = "Your Name", email = "your.email@example.com" }]
dependencies = ["pydaconf"]

[project.entry-points.pydaconf.plugins]
custom = "myplugin.custom_plugin:CustomPlugin"
```

### Define the Plugin Module Structure

Your package should follow this structure:

```
pydaconf-plugins-custom/
│── myplugin/
│   ├── __init__.py
│   ├── custom_plugin.py  # Contains the CustomPlugin class
│── pyproject.toml
│── README.md
```

## 3. Installing and Using the Plugin Locally

To install the packaged plugin locally:

```sh
pip install .
```

Once installed, PydaConf will automatically detect and load the plugin when needed.

## 4. Deploying the Plugin to PyPI

To publish the plugin to [PyPI](https://pypi.org/), follow these steps:

```sh
pip install flit
flit publish
```
This will build and upload the package to PyPI, making it publicly available for installation.

> **Note:** You will need to setup your ~/.pypirc or provide the required environment variables. You can read the flit documentation [Flit](https://flit.pypa.io/en/stable/upload.html#using-pypirc)

> **Note:** You can integrate this process into any CI/CD system to automate deployment.

## Next Steps

Learn more about **[Installing Plugins](install_plugins.md)** to manage and distribute your custom plugins!

