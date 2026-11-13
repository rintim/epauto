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
    retry_periods: dict[LoopState, int | None] = {
        LoopState.LOGIN: None,
        LoopState.CONNECT: None,
    }

    async with ClientSession(headers={"User-Agent": cfg.base.user_agent}) as session:
        while True:
            match state:
                case LoopState.INIT:
                    logger.info("Starting execution loop.")
                    state = LoopState.CHECK
                    continue
                case LoopState.CHECK:
                    state = await check.execute(cfg, session)
                    if state == LoopState.CONNECT:
                        retry_periods[LoopState.LOGIN] = None
                    if state == LoopState.LOGIN:
                        retry_periods[LoopState.CONNECT] = None
                    if retry_periods[state] is not None and retry_periods[state] > 0:
                        logger.info(
                            "Retrying %s in %d seconds...",
                            state.name,
                            retry_periods[state],
                        )
                        await asyncio.sleep(retry_periods[state])
                    continue
                case LoopState.LOGIN:
                    next_state = await login.execute(cfg, session)
                case LoopState.CONNECT:
                    next_state, connected_for = await connect.execute(cfg, session)
                    if next_state == LoopState.CONNECT:
                        retry_periods[state] = None
                        continue
                    if connected_for > max(cfg.base.retry_period, retry_periods[state] or 0):
                        retry_periods[state] = None

            retry_periods[state] = min(
                retry_periods[state] + cfg.base.retry_period_diff
                if retry_periods[state] is not None
                else cfg.base.retry_period,
                cfg.base.retry_period_max,
            )
            state = next_state
