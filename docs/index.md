![logo](logo.png)

# Welcome to PydaConf
**PydaConf** is a lightweight yet powerful open-source Python library for loading application configurations. It leverages modern Python features, including type hints and Pydantic models, for clarity and maintainability.

# Features
✅ Load configurations from YAML, TOML, and JSON  
✅ Pydantic integration for robust validation  
✅ Dynamic secret injection via a pluggable architecture  
✅ String interpolation for flexible configurations  
✅ Built-in plugins for environment variables, sealed secrets, and file-based secrets  
✅ OnUpdate callbacks for updated configuration values  

# Why Choose PydaConf?
* **Simple and Intuitive**: Easy-to-use API for managing configurations.
* **Secure and Extensible**: Supports encrypted secrets and custom plugins.
* **Flexible and Modern**: Uses Python's latest features and best practices.

# Quick Example
* Create config file in toml, yaml or json
```yaml
domain: pydaconf.com
openai_token: ENV:///OPENAI_TOKEN
database:
  host: eu-central-db01.{{ domain }}
  username: svc_db01
  password: SEALED:///gAAAAABnpRqHdho_dFB7iMs_Ufv5nu59LwqQfE3YCjaDTyg-YrYsEpK8bfvdKsdrj6kCxrAjezCGAdVM0FhzwyfYFIgqnquw8w==
```

* Create Pydantic Model and load the configuration
```python
from pydaconf import PydaConf
from pydantic import BaseModel

class DbConfig(BaseModel):
    host: str
    username: str
    password: str

class Config(BaseModel):
    domain: str
    openai_token: str
    database: DbConfig

provider = PydaConf[Config]()
provider.from_file("config.yaml")
print(provider.config.database.password)
```