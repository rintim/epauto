import asyncio
import logging
from aiohttp import ClientSession

from . import check, connect, login
from .state import LoopState
from ..config import Config

__all__ = ["execute"]
logger = logging.getLogger(__name__)


async def execute(cfg: Config):
    state = LoopState.INIT

    header = {
        "User-Agent": cfg.base.user_agent,
    }
    EXECUTOR_MAP = {
        # LoopState.INIT: None,
        LoopState.CHECK: check.execute,
        LoopState.LOGIN: login.execute,
        LoopState.CONNECT: connect.execute,
    }

    async with ClientSession(headers=header) as session:
        while True:
            match state:
                case LoopState.INIT:
                    # In fact I don't know what to write here
                    # Remain for future
                    # Currently just transition to CHECK
                    logger.info("Starting execution loop.")
                    state = LoopState.CHECK
                case _:
                    executor = EXECUTOR_MAP[state]
                    if executor is None:
                        logger.error(
                            f"No executor defined for state: {state}. Exiting loop."
                        )
                        break

                    logger.debug(f"Executing state: {state}.")
                    next_state = await executor(cfg, session)
                    state = next_state

    logger.debug("Execution loop has ended.")
    loop = asyncio.get_event_loop()
    loop.stop()
