import asyncio
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
@click.version_option(message="%(package)s %(version)s")
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
    except KeyError as e:
        click.echo(f"Error: Missing required configuration field: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: Failed to load configuration: {e}", err=True)
        sys.exit(1)

    loop = bootstrap()
    main_task = loop.create_task(execute(cfg))

    try:
        loop.run_forever()
    finally:
        if not main_task.done():
            main_task.cancel()
        loop.run_until_complete(asyncio.gather(main_task, return_exceptions=True))
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
