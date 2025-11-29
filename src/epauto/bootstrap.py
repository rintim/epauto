""" """

__all__ = ["bootstrap"]


def bootstrap() -> None:
    set_logger()
    set_signal()


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


def set_signal() -> None:
    import signal
    import sys

    signal.signal(signal.SIGINT, lambda *_: sys.exit())
    signal.signal(signal.SIGTERM, lambda *_: sys.exit())
