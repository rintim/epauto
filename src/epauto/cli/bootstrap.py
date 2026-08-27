""" """

import asyncio

__all__ = ["bootstrap"]


def bootstrap() -> asyncio.AbstractEventLoop:
    loop = asyncio.new_event_loop()

    set_logger()
    set_signal(loop)

    return loop


def set_logger() -> None:
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": "INFO",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": True,
            },
        },
    }

    from logging.config import dictConfig

    dictConfig(config)


def set_signal(loop: asyncio.AbstractEventLoop) -> None:
    import signal

    shutdown_task = None

    async def exit_app():
        current_task = asyncio.current_task(loop)
        tasks = [task for task in asyncio.all_tasks(loop) if task is not current_task]

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

        loop.stop()

    def handler():
        nonlocal shutdown_task
        if shutdown_task is None or shutdown_task.done():
            shutdown_task = loop.create_task(exit_app())

    loop.add_signal_handler(signal.SIGINT, handler)
    loop.add_signal_handler(signal.SIGTERM, handler)
