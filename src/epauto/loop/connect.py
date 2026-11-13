import asyncio
import logging
from aiohttp import (
    ClientSession,
    ClientWebSocketResponse,
    WSMsgType,
)

from .state import LoopState
from ..config import Config

__all__ = ["execute"]
logger = logging.getLogger(__name__)


async def execute(cfg: Config, session: ClientSession) -> tuple[LoopState, float]:
    loop = asyncio.get_running_loop()
    connected_at = None
    try:
        async with asyncio.timeout(cfg.connect.connect_ping_timeout):
            ws = await session.ws_connect(
                cfg.connect.connect_url,
                heartbeat=cfg.connect.connect_ping_interval,
            )
        connected_at = loop.time()
        async with ws:
            auto_closed = await connect_handler(ws, cfg)
    except Exception as e:
        logger.error('WebSocket connection failed: %s("%s")', type(e).__name__, e)
        return LoopState.CHECK, 0 if connected_at is None else loop.time() - connected_at

    return (
        LoopState.CONNECT if auto_closed else LoopState.CHECK,
        loop.time() - connected_at,
    )


async def connect_handler(ws: ClientWebSocketResponse, cfg: Config) -> bool:
    """
    Keeps the connection alive until it ends.

    Returns:
        bool: True if the connection was ended by auto-close, False if it was
            closed by the server.
    """

    logger.info("WebSocket connection established.")

    auto_close_after = (
        cfg.connect.auto_close.duration if cfg.connect.auto_close.enable else None
    )
    auto_close: asyncio.Timeout | None = None
    try:
        async with asyncio.timeout(auto_close_after) as auto_close:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    logger.info("Received message: %s", msg.data)
                elif msg.type == WSMsgType.ERROR:
                    raise Exception(f"WebSocket error: {msg.data}")

    except TimeoutError:
        # Only our own auto-close deadline counts; any other timeout is a
        # connection failure for the caller to handle.
        if auto_close is None or not auto_close.expired():
            raise

        logger.info(
            "Auto-close duration (%d seconds) reached. Closing and reconnecting...",
            auto_close_after,
        )
        return True

    return False
