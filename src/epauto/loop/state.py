from enum import Enum, auto

__all__ = ["LoopState"]


class LoopState(Enum):
    INIT = auto()
    CHECK = auto()
    LOGIN = auto()
    CONNECT = auto()
