"""
epauto - A simple auto-login script for Eportal.

Copyright (c) 2025 Rintim. Licensed under MIT License.
"""

import sys
import click
from pathlib import Path
from typing import Optional

from .bootstrap import bootstrap
from .config import Config

__all__ = ["__version__", "main"]
__version__ = "0.3.0"


@click.command()
@click.option(
    "--config",
    type=click.Path(path_type=Path),
    default="config.toml",
    help="Path to configuration file.",
)
@click.option("--version", is_flag=True, help="Print epauto version.")
def main(version: bool, config: Path) -> None:
    if version:
        print_version()
        return

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

    bootstrap()


def print_version():
    version = f"epauto {__version__}"
    click.echo(version)
