<p align="center">
  <a href="https://github.com/varadinov/pydaconf"><img src="https://raw.githubusercontent.com/varadinov/pydaconf/refs/heads/main/logo.png" alt="Pydaconf"></a>
</p>

<p align="center">
    <em>Modern python configuration file manager using  <a href="https://docs.pydantic.dev/latest/">Pydantic</a> and python type hints.</em>
</p>

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/varadinov/pydaconf/ci.yaml)
![GitHub last commit](https://img.shields.io/github/last-commit/varadinov/pydaconf)
![GitHub](https://img.shields.io/github/license/varadinov/pydaconf)
[![GitHub](https://varadinov.github.io/pydaconf/coverage.svg)](https://varadinov.github.io/pydaconf/)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://varadinov.github.io/pydaconf/)


## What is PydaConf
Pydaconf is a simple yet powerful open-source Python library for loading application configurations. It leverages modern Python features, including type hints and the awesome data validation Pydantic models for clarity and maintainability. Pydaconf provides seamless configuration loading from YAML, TOML, and JSON files while supporting dynamic secret injection via a pluggable architecture.

## Installation
Install using `pip install pydaconf[all]`  
For more installation options see the [Install](https://https://varadinov.github.io/pydaconf/) section in the documentation.


## A Simple Example
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

## Help
See [documentation](https://https://varadinov.github.io/pydaconf/) for more details.

## Interpolation

| Templates Example                      |
|----------------------------------------|
| contact_email: user@{{ domain }}       | 
| db_server: {{ backend.server }}        |
| first_username: {{ users[0].username }} |


## Builtin plugins
| Plugin        | Description                                                                                                                                                       |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ENV           | Inject secret from environment variable                                                                                                                           |
| SEALED        | Inject a sealed secret. Secrets can be encrypted with a symmetric key and stored in a file. The provider expects the key in the PYDACONF_SEALED_KEY environment variable. |
| FILE_CONTENT  | Inject content from a file. This is useful in scenarios where the secret is mounted on the file system, such as in k8s containers.                                | 

## Official plugins
| Plugin        | Description                |
|---------------|----------------------------|
|            |  |
