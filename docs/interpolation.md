# Interpolating Strings in PydaConf

PydaConf supports **string interpolation**, allowing configuration values to be dynamically composed using placeholders. This is useful for injecting values from other configuration fields, making configurations more flexible and reusable.

## Interpolation Syntax

Placeholders follow the **Jinja-like** syntax:

```yaml
key: "{{ variable_name }}"
```

Placeholders reference other fields in the configuration file.

## Example Configuration with Interpolation

### YAML Example (`config.yaml`)
```yaml
domain: example.com
api_base_url: "https://api.{{ domain }}"
user_email: "admin@{{ domain }}"
```

### TOML Example (`config.toml`)
```toml
domain = "example.com"
api_base_url = "https://api.{domain}"
user_email = "admin@{domain}"
```

### JSON Example (`config.json`)
```json
{
  "domain": "example.com",
  "api_base_url": "https://api.{{ domain }}",
  "user_email": "admin@{{ domain }}"
}
```

## Using PydaConf to Resolve Interpolation

```python
from pydaconf import PydaConf
from pydantic import BaseModel

class Config(BaseModel):
    domain: str
    api_base_url: str
    user_email: str

provider = PydaConf[Config]()
provider.from_file("config.yaml")

print(provider.config.api_base_url)  # Output: https://api.example.com
print(provider.config.user_email)  # Output: admin@example.com
```

## Handling Nested Interpolation

PydaConf allows placeholders inside nested structures:

```yaml
database:
  host: "db.{{ domain }}"
  url: "postgres://{{ database.host }}/mydb"
```

These placeholders are resolved in multiple passes to ensure dependencies are correctly substituted.

## Next Steps

Check out how **[Plugins](plugins.md)** can extend PydaConf with external data sources!

