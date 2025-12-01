"""
Encapsulations for http requests.

There's only JSONP request which is needed to encapsulate.
"""

import math
from aiohttp import ClientSession, ClientTimeout
from collections import deque
from random import random
from typing import Optional
from urllib.parse import quote_plus, urlparse

from .jsonp import decode

__all__ = ["jsonp"]


async def jsonp(
    url: str,
    name: str,
    params: Optional[dict[str, str]] = None,
    headers: Optional[dict[str, str]] = None,
) -> dict:
    """
    Fetches a JSONP response from the given URL with parameters and decodes it.

    Args:
            url (str): The URL to send the GET request to.
            callback_name (str): The expected JSONP callback name.
            params (Optional[dict[str, str]], optional): The query parameters for the GET request.
            headers (Optional[dict[str, str]], optional): The headers for the GET request.

    Returns:
            dict: The decoded JSON data.
    """

    # So, due to some tricky aspects of the original connection,
    # the parameter addresses are pieced together by backport logic.
    data = {"callback": name, "jsVersion": "4.1.3"}
    if params is not None:
        data.update(params)

    param_strs = deque()
    for key in data:
        content = f"{quote_plus(key)}={quote_plus(data[key])}"
        if key == "callback":
            param_strs.appendleft(content)
        else:
            param_strs.append(content)
    param_strs.append(f"v={math.floor(random() * 10000 + 500)}")
    param_strs.append("lang=zh")
    param_url = "&".join(param_strs)

    full_url = None
    parsed_url = urlparse(url)
    if len(parsed_url.query) > 0:
        full_url = f"{url}&{param_url}"
    else:
        full_url = f"{url}?{param_url}"

    async with ClientSession(
        headers=headers, timeout=ClientTimeout(total=5)
    ) as session:
        async with session.get(full_url) as response:
            text = await response.text()
            return decode(text, name=name)
