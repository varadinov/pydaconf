# Plugins in PydaConf

PydaConf supports a **pluggable architecture**, allowing users to inject dynamic values into configurations from external sources such as environment variables, encrypted secrets, and files.

## Built-in Plugins

PydaConf includes several built-in plugins:

| Plugin         | Description  |
|---------------|--------------|
| **ENV**       | Loads secrets from environment variables. |
| **SEALED**    | Handles encrypted secrets using a symmetric key. |
| **FILE_CONTENT** | Reads content from a file (useful for mounted secrets in containers). |

## Using Plugins in Configuration Files

You can reference plugins in your configuration files using a `PREFIX:///VALUE` syntax.

### Example: Environment Variables

```yaml
api_key: ENV:///API_KEY
```

If the `API_KEY` environment variable is set, PydaConf will inject its value.

### Example: Sealed Secrets

```yaml
database_password: SEALED:///gAAAAABnp...
```

Decryption requires setting `PYDACONF_SEALED_KEY` as an environment variable.

### Example: File Content

```yaml
cert_content: FILE_CONTENT:///path/to/cert.pem
```

## Registering Custom Plugins

You can develop and register your own local custom plugins.

```python
from pydaconf.plugins.base import PluginBase
from collections.abc import Callable

class CustomPlugin(PluginBase):
    PREFIX = "CUSTOM"
    
    def run(self, value: str, on_update_callback: Callable[[str], None]) -> str:
        return f"Processed {value}"
```

To use the custom plugin:

```python
provider = PydaConf[Config]()
provider.register_plugin(CustomPlugin)
```

## Next Steps

Learn how to **[Develop and Package Plugin](plugins/develop_and_package_plugin.md)** and extend PydaConf further!

