import asyncio
import sys
import click
from pathlib import Path

from .bootstrap import bootstrap
from ..config import Config
from ..loop import execute

__all__ = ["run"]


def run(config: Path) -> None:
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
    shutting_down = False

    def stop_on_completion(task):
        if not shutting_down:
            loop.stop()

    main_task.add_done_callback(stop_on_completion)

    try:
        loop.run_forever()
    finally:
        shutting_down = True
        main_task.remove_done_callback(stop_on_completion)
        if not main_task.done():
            main_task.cancel()
        loop.run_until_complete(asyncio.gather(main_task, return_exceptions=True))
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

    if not main_task.cancelled():
        try:
            main_task.result()
        except Exception as e:
            raise click.ClickException(f"Execution failed: {e}") from e
