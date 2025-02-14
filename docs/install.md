# Installation

## Installing PydaConf

PydaConf is available on PyPI and can be installed using `pip`:

```bash
pip install pydaconf
```

### Installing with Optional Dependencies

PydaConf provides additional features through optional dependencies:

- **YAML Support** (for `.yaml` and `.yml` files):

```bash
pip install pydaconf[yaml]
```

- **TOML Support** (for `.toml` files for python versions before 3.11):

```bash
pip install pydaconf[toml]
```

- **Requests Support** (for loading configurations from URLs):

```bash
pip install pydaconf[requests]
```
[index.md](index.md)
- **Sealed Secrets** (for encrypted secrets handling):

```bash
pip install pydaconf[cryptography]
```

- **CLI Support**:

```bash
pip install pydaconf[cli]
```

To install all optional dependencies at once:

```bash
pip install pydaconf[all]
```

## Verifying Installation

To confirm that PydaConf is installed correctly, run:

```bash
python -c "import pydaconf; print(pydaconf.__version__)"
```

If the installation was successful, this command will output the installed version of PydaConf.

## Next Steps

Now that you have installed PydaConf, check out [**Config Files**](config_files.md) to start managing your configurations!

