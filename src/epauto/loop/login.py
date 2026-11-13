import logging
from aiohttp import ClientSession, ClientTimeout

from .state import LoopState
from ..config import Config, LoginType
from ..lib.base import encode
from ..lib.request import jsonp

__all__ = ["execute"]
logger = logging.getLogger(__name__)


async def execute(cfg: Config, session: ClientSession) -> LoopState:

    try:
        message = await execute_path_of_pain(cfg, session)

        logger.info(message)

    except Exception as e:
        logger.error(
            "Login failed: %s",
            str(e).replace(cfg.login.password, "[REDACTED]")
            if type(e) is Exception
            else type(e).__name__,
        )

    return LoopState.CHECK


async def execute_path_of_pain(cfg: Config, session: ClientSession) -> str:
    root = cfg.login.url.root
    portal_api = cfg.login.url.portal_api
    path_url = cfg.login.url.path

    header = {
        "User-Agent": cfg.base.user_agent,
        "Accept": "*/*",
    }

    logger.info("Attempting to init page environment...")
    await address_root_page(root, header, session)

    login_method = await load_config(portal_api, header, session)
    logger.info("Fetched configuration data.")

    online, info = await check_status(path_url, header, session)
    if online:
        return info

    ip = info
    logger.info("Fetched IP info: %s", ip)

    base_url = path_url if login_method == 0 else portal_api
    await login(ip, cfg, base_url, login_method, header, session)
    return "Login successful."


async def address_root_page(
    root: str, header: dict[str, str], session: ClientSession
) -> None:
    try:
        async with session.get(
            root, headers=header, timeout=ClientTimeout(total=5)
        ) as response:
            if response.status == 200:
                logger.info("Page environment initialized.")
            else:
                raise Exception(f"Unexpected status code: {response.status}")
    except TimeoutError:
        raise Exception(f"Connection to {root} timed out.")


async def load_config(
    portal_api: str, header: dict[str, str], session: ClientSession
) -> int:
    url = f"{portal_api}page/loadConfig"
    params = {
        "program_index": "I352nd1630892431",
        "wlan_vlan_id": "1",
        "wlan_user_ip": encode("000.000.000.000"),
        "wlan_user_ipv6": encode(""),
        "wlan_user_ssid": "",
        "wlan_user_areaid": "",
        "wlan_ac_ip": encode(""),
        "wlan_ap_mac": "000000000000",
        "gw_id": "000000000000",
    }

    cfg = None
    try:
        cfg = await jsonp(session, url, "dr1001", params, header)
    except TimeoutError:
        raise Exception(f"Connection to {url} timed out.")

    if cfg["code"] != 1:
        raise Exception("Failed to fetch portal configuration.")

    return cfg["data"]["login_method"]


async def check_status(
    path: str, header: dict[str, str], session: ClientSession
) -> tuple[bool, str]:
    url = f"{path}chkstatus"

    data = None
    try:
        data = await jsonp(session, url, "dr1002", headers=header)
    except TimeoutError:
        raise Exception(f"Connection to {url} timed out.")

    if data["result"] == 1:
        return (True, "System is online.")
    else:
        return (False, data["v46ip"])


async def login(
    ip: str,
    cfg: Config,
    base_url: str,
    login_method: int,
    header: dict[str, str],
    session: ClientSession,
) -> None:
    login_url = f"{base_url}login"

    username = None
    if cfg.login.type == LoginType.CAMPUS:
        username = cfg.login.username
    else:
        username = f"{cfg.login.username}@{cfg.login.type.get_suffix()}"
    params = {
        "login_method": str(login_method),
        "user_account": username,
        "user_password": cfg.login.password,
        "wlan_user_ip": ip,
        "wlan_user_ipv6": "",
        "wlan_user_mac": "000000000000",
        "wlan_ac_ip": "",
        "wlan_ac_name": "",
        "terminal_type": "1",
    }

    result = None
    try:
        result = await jsonp(session, login_url, "dr1003", params, header)
    except TimeoutError:
        raise Exception(f"Connection to {login_url} timed out.")

    if result["result"] != 1:
        raise Exception("Portal rejected login.")
