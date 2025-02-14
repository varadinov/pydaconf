# Config Files

PydaConf allows loading configurations from various file formats, including **YAML, TOML, and JSON**. This flexibility enables seamless integration into different applications and environments.

## Supported Formats

PydaConf automatically detects and parses configuration files based on their format:

| Format | File Extension | Parser Used                                     |
|--------|---------------|-------------------------------------------------|
| YAML   | `.yaml`, `.yml` | PyYAML                                          |
| TOML   | `.toml` | tomli (<3.11) or tomllib (Python 3.11+)  |
| JSON   | `.json` | Python's built-in JSON module                   |

## Example Configuration Files

### YAML Configuration (`config.yaml`)
```yaml
domain: example.com
database:
  host: db.example.com
  username: admin
  password: ENV://DB_PASSWORD
```

### TOML Configuration (`config.toml`)
```toml
domain = "example.com"

[database]
host = "db.example.com"
username = "admin"
password = "ENV://DB_PASSWORD"
```

### JSON Configuration (`config.json`)
```json
{
  "domain": "example.com",
  "database": {
    "host": "db.example.com",
    "username": "admin",
    "password": "ENV://DB_PASSWORD"
  }
}
```

## Loading Configuration Files

Use PydaConf to load configuration files seamlessly:

```python
from pydaconf import PydaConf
from pydantic import BaseModel

class DatabaseConfig(BaseModel):
    host: str
    username: str
    password: str

class Config(BaseModel):
    domain: str
    database: DatabaseConfig

provider = PydaConf[Config]()
provider.from_file("config.yaml")
print(provider.config.database.host)  # Output: db.example.com
```

## Next Steps

Learn how to use **[Values Interpolation](interpolation.md)** to make your configurations more dynamic!

