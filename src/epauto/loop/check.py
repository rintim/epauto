import logging
from aiohttp import ClientSession, ClientTimeout

from .state import LoopState
from ..config import Config

__all__ = ["execute"]
logger = logging.getLogger(__name__)


async def execute(cfg: Config) -> LoopState:
    logger.info("Try to check connectivity...")
    try:
        header = {
            "User-Agent": cfg.base.user_agent,
        }

        async with ClientSession(
            headers=header, timeout=ClientTimeout(total=cfg.connect.test_timeout)
        ) as session:
            try:
                async with session.get(cfg.connect.test_url) as response:
                    if response.status == 200:
                        logger.info("Already connected to the internet.")
                        return LoopState.CONNECT
                    else:
                        raise Exception(f"Unexpected status code: {response.status}")
            except TimeoutError:
                raise Exception(f"Connection to {cfg.connect.test_url} timed out.")

    except Exception as e:
        logger.info('Check failed: [%s]"%s". Proceeding to login.', type(e).__name__, e)
        return LoopState.LOGIN
