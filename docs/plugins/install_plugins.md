# Installing Plugins in PydaConf

PydaConf supports external plugins to extend its functionality. Plugins follow the naming convention:

```
pydaconf-plugins-<name>
```

For example, a Kubernetes-related plugin might be named:

```
pydaconf-plugins-k8s
```

## Installing a Plugin

Plugins are distributed as Python packages and can be installed using `pip`:

```sh
pip install pydaconf-plugins-<name>
```

### Example: Installing the Kubernetes Plugin

To install the **pydaconf-plugins-k8s** plugin:

```sh
pip install pydaconf-plugins-k8s
```

Once installed, the plugin will be automatically discovered and loaded by PydaConf.

## Verifying Installed Plugins

You can list installed PydaConf plugins using the following command:

```sh
pip list | grep pydaconf-plugins
```

Alternatively, you can programmatically check loaded plugins:

```python
from pydaconf.utils.plugins import load_dynamic_plugins

for plugin in load_dynamic_plugins():
    print(plugin.PREFIX)
```

## Next Steps

Learn how to **[Develop and Package Plugin](develop_and_package_plugin.md)** to create custom integrations!

