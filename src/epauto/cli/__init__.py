import click
from pathlib import Path


@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(path_type=Path),
    default="config.toml",
    help="Path to configuration file.",
)
@click.version_option(None, "-v", "--version", message="%(package)s %(version)s")
def main(config: Path):
    from .app import run

    run(config)
