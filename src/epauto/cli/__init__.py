import sys
import click
from pathlib import Path

from .. import __version__
from .bootstrap import bootstrap
from ..config import Config
from ..loop import execute


@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(path_type=Path),
    default="config.toml",
    help="Path to configuration file.",
)
@click.version_option(
    __version__, package_name="epauto", message="%(package)s %(version)s"
)
def main(config: Path):
    if not config.exists():
        click.echo(
            f"Error: Configuration file '{config}' does not exist.",
            err=True,
        )
        sys.exit(1)

    cfg = None
    try:
        cfg = Config.init(config)
    except ValueError as e:
        click.echo(f"Error: Failed to load configuration: {e}", err=True)
        sys.exit(1)

    loop = bootstrap()

    try:
        loop.create_task(execute(cfg))
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
