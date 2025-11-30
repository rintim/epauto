"""
Structs and utility functions to load toml config for epauto.
"""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse


@dataclass
class Config:
    base: BaseConfig
    login: LoginConfig
    connect: ConnectConfig

    @staticmethod
    def init(path: Path) -> Config:
        """
        Initializes configuration from a toml file.

        Args:
            path (Path): Path to the toml configuration file.

        Raises:
            ValueError: If required configuration fields are missing.

        Returns:
            Config: The initialized configuration object.
        """

        from . import __version__

        data = None
        with path.open("rb") as f:
            data = tomllib.load(f)

        # Base
        base: dict[str, Any] = data.get("base", {})

        user_agent = base.get("user_agent", f"epauto/{__version__}")
        retry_period = base.get("retry_period", 5)
        retry_period_diff = base.get("retry_period_diff", 5)
        retry_period_max = base.get("retry_period_max", 300)
        base_cfg = BaseConfig(
            user_agent=user_agent,
            retry_period=retry_period,
            retry_period_diff=retry_period_diff,
            retry_period_max=retry_period_max,
        )

        # Login
        login: Optional[dict[str, Any]] = data["login"]
        if login is None:
            raise ValueError("login section is required in configuration.")
        if "url" not in login:
            raise ValueError("login.url is required in configuration.")
        if "username" not in login or "password" not in login:
            raise ValueError(
                "login.username and login.password are required in configuration."
            )

        login_cfg = LoginConfig(
            url=LoginURL(login["url"]),
            username=login["username"],
            password=login["password"],
        )

        # connect
        connect: dict[str, Any] = data.get("connect", {})

        test_url = connect.get("test_url", "https://www.baidu.com")
        test_timeout = connect.get("test_timeout", 5)
        connect_url = connect.get("connect_url", "wss://echo.websocket.org")
        connect_ping_interval = connect.get("connect_ping_interval", 10)
        connect_ping_timeout = connect.get("connect_ping_timeout", 5)

        # auto_close
        auto_close = connect.get("auto_close", {})

        auto_close_enable = auto_close.get("enable", False)
        auto_close_duration = auto_close.get("duration", 570)

        auto_close_cfg = ConnectAutoCloseConfig(
            enable=auto_close_enable,
            duration=auto_close_duration,
        )
        connect_cfg = ConnectConfig(
            test_url=test_url,
            test_timeout=test_timeout,
            connect_url=connect_url,
            connect_ping_interval=connect_ping_interval,
            connect_ping_timeout=connect_ping_timeout,
            auto_close=auto_close_cfg,
        )

        return Config(base=base_cfg, login=login_cfg, connect=connect_cfg)


@dataclass
class BaseConfig:
    user_agent: str
    retry_period: int
    retry_period_diff: int
    retry_period_max: int


@dataclass
class LoginConfig:
    url: LoginURL
    username: str
    password: str


@dataclass
class ConnectConfig:
    test_url: str
    test_timeout: int
    connect_url: str
    connect_ping_interval: int
    connect_ping_timeout: int
    auto_close: ConnectAutoCloseConfig


@dataclass
class ConnectAutoCloseConfig:
    enable: bool
    duration: int


@dataclass(init=False)
class LoginURL:
    root: str
    host: str
    path: str
    eportal: str
    portal_api: str

    def __init__(self, root: str) -> None:
        self.root = root
        self.update_suburls()

    def update_suburls(self) -> None:
        url = urlparse(self.root)
        port = 802 if url.scheme == "https" else 801

        self.host = f"{url.scheme}://{url.hostname}/"
        if url.port is not None:
            self.host = f"{url.scheme}://{url.hostname}:{url.port}/"
        self.path = f"{self.host}drcom/"

        self.eportal = f"{url.scheme}://{url.hostname}:{port}/eportal/"
        self.portal_api = f"{self.eportal}portal/"
