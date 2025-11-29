"""
epauto - A simple auto-login script for Eportal.

Copyright (c) 2025 Rintim. Licensed under MIT License.
"""

import click
from pathlib import Path
from typing import Optional

__all__ = ["__version__", "main"]
__version__ = "0.3.0"


@click.command()
@click.option(
    "--config", type=click.Path(path_type=Path), help="Path to configuration file."
)
@click.option("--version", is_flag=True, help="Print epauto version.")
def main(version: bool, config: Optional[Path]):
    if version:
        print_version()
        return

    # TODO: Implement the main functionality here


def print_version():
    version = f"epauto {__version__}"
    click.echo(version)
