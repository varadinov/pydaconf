# PydaConf Sealed Secrets Guide

The Sealed Plugin in PydaConf allows storing and retrieving encrypted secrets securely within configuration files. It uses symmetric encryption, making it ideal for managing sensitive information like API keys, passwords, and tokens.

## How It Works
* Secrets are encrypted before being stored in configuration files.
* PydaConf automatically decrypts them at runtime using an encryption key.
* This ensures that sensitive data is never stored in plain text.

## Install Dependencies
Ensure PydaConf and its encryption dependencies are installed:
```bash
pip install pydaconf[cryptography]
pip install pydaconf[cli]
```

## Sealed Secrets Management using the CLI

The `seal` command group provides functionality for managing encrypted secrets.

### 1. Generating an Encryption Key

```sh
pydaconf seal generate-key
```

This command generates a symmetric encryption key for sealed secrets, which should be stored securely.

### 2. Encrypting a Secret

```sh
pydaconf seal encrypt --key <your-key> --secret "my-secret-value"
```

Example:

```sh
pydaconf seal encrypt --key abc123xyz --secret "super-secret-password"
```
This outputs an encrypted string, which can be stored in your configuration file:

```yaml
database:
  password: SEALED:///gAAAAABnp...
```
## Using the Sealed Plugin in PydaConf
> **Note** Decryption requires setting `PYDACONF_SEALED_KEY` as an environment variable before staring you application.

When PydaConf loads the configuration, it automatically decrypts the SEALED:/// values using the key from `PYDACONF_SEALED_KEY`:

```python
from pydaconf import PydaConf
from pydantic import BaseModel

class Config(BaseModel):
    database_password: str

provider = PydaConf[Config]()
provider.from_file("config.yaml")
print(provider.config.database_password)  # Decrypted value
```



## Next Steps

Explore more on **[Developing and Packaging Plugins](../plugins/develop_and_package_plugin.md)** to extend PydaConf’s capabilities!

