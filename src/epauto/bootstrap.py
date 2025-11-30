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

    async def exit_app():
        tasks = asyncio.all_tasks(loop)

        for task in tasks:
            task.cancel()

        for task in tasks:
            try:
                await task
            except asyncio.CancelledError:
                pass

        loop.stop()

    def handler():
        asyncio.ensure_future(exit_app())

    loop.add_signal_handler(signal.SIGINT, handler)
    loop.add_signal_handler(signal.SIGTERM, handler)
