# Subscribing to Configuration Updates with `on_update`

PydaConf provides an `on_update` mechanism that allows you to subscribe to specific configuration value updates. This is useful when you need to react dynamically to changes in your configuration.

## Using `on_update`

You can subscribe to configuration changes by specifying a key pattern and a callback function that will be triggered when the value is updated.

### Example: Subscribing to a Value Update

```python
from pydaconf import PydaConf
from pydantic import BaseModel

def on_change_callback(key: str, value: str):
    print(f"Configuration updated: {key} -> {value}")

class Config(BaseModel):
    api_key: str
    database_url: str

provider = PydaConf[Config]()
provider.from_file("config.yaml")

# Subscribe to updates for api_key
provider.on_update(".api_key", on_change_callback)
```

### Example: Handling Nested Keys
You can use regex to subscribe for specific updates.

```python
def nested_callback(key: str, value: str):
    print(f"Nested key updated: {key} -> {value}")

provider.on_update(".database.*", nested_callback)
```

This pattern allows you to watch all keys under `database`. Whenever any nested value changes, the callback will be triggered.

## Next Steps

Learn more about **[Interpolation](interpolation.md)** to make your configuration more dynamic!

