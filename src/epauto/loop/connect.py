import asyncio
import logging
from aiohttp import (
    ClientSession,
    ClientTimeout,
    ClientWebSocketResponse,
    WSMsgType,
)

from .state import LoopState
from ..config import Config

__all__ = ["execute"]
logger = logging.getLogger(__name__)


async def execute(cfg: Config) -> LoopState:
    timeout = ClientTimeout(total=cfg.connect.connect_ping_timeout)

    header = {
        "User-Agent": cfg.base.user_agent,
    }

    while True:
        try:
            async with ClientSession(headers=header, timeout=timeout) as session:
                async with session.ws_connect(
                    cfg.connect.connect_url,
                    heartbeat=cfg.connect.connect_ping_interval,
                ) as ws:
                    await connect_handler(ws, cfg)
        except TimeoutError:
            logger.error("WebSocket connection Timeout.")
            return revert_to_checking()

        except Exception as e:
            logger.error('WebSocket connection failed: %s("%s")', type(e).__name__, e)
            return revert_to_checking()


async def connect_handler(ws: ClientWebSocketResponse, cfg: Config) -> None:
    logger.info("WebSocket connection established.")

    timeout = cfg.connect.auto_close.duration if cfg.connect.auto_close.enable else None
    try:
        async with asyncio.timeout(timeout):
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    logger.info("Received message: %s", msg.data)
                elif msg.type == WSMsgType.ERROR:
                    raise Exception(f"WebSocket error: {msg.data}")

    except asyncio.TimeoutError:
        logger.info("The Server is closing the connection. Close and reconnecting...")


def revert_to_checking() -> LoopState:
    logger.info("Reverting to CHECK state.")
    return LoopState.CHECK
