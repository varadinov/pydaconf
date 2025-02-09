try:
    import typer
    from cryptography.fernet import Fernet
except ImportError as e:
    raise ImportError('CLI dependencies are not installed, run `pip install pydaconf[cli]`') from e

app = typer.Typer()
seal = typer.Typer()
app.add_typer(seal, name="seal")

# TODO: Add better error handling

@seal.command('generate-key')
def generate_key() -> None:
    """Generate symmetric encryption key for sealed secrets"""
    typer.echo(Fernet.generate_key().decode())

@seal.command('encrypt')
def generate(key: str, secret: str) -> None:
    """Encrypt secret with symmetric encryption key"""
    f = Fernet(key)
    typer.echo(f.encrypt(secret.encode()).decode())

@seal.command('decrypt')
def decrypt(key: str, secret: str) -> None:
    """Encrypt secret with symmetric encryption key"""
    f = Fernet(key)
    typer.echo(f.decrypt(secret).decode())


if __name__ == "__main__":
    app()