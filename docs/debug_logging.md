# Enable Debug Logging in PydaConf

Debug logging is useful for troubleshooting and understanding the internal behavior of PydaConf. You can enable debug logging using either of the following methods:

## Option 1: Basic Debug Logging

The simplest way to enable debug logging is by configuring the root logger using `logging.basicConfig`:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Pros:
- Simple and quick to set up.
- Enables debug logging for all loggers in the application.

### Cons:
- May produce excessive logs if other libraries also log at the debug level.
- Less control over log formatting and output destinations.

## Option 2: Configuring a Named Logger

For more control over logging output and formatting, configure a named logger specifically for PydaConf:

```python
import logging

logger = logging.getLogger('pydaconf')
logger.setLevel(logging.DEBUG)

fh = logging.StreamHandler()
fh_formatter = logging.Formatter('%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s')
fh.setFormatter(fh_formatter)

logger.addHandler(fh)
```

### Pros:
- Provides detailed control over log formatting.
- Limits debug logging to PydaConf without affecting other loggers.
- Allows additional handlers (e.g., file logging) if needed.

### Cons:
- Requires more setup compared to `basicConfig`.

## Choosing the Right Option
- Use **Option 1** if you need quick debugging for all loggers.
- Use **Option 2** if you need more control over PydaConf logging specifically.

By enabling debug logging, you can gain better insights into PydaConf's behavior and troubleshoot issues effectively.