"""
Simple JSONP library.

This module just provides a JSONP decoder for no encoder needed.
"""

import json
from typing import Any, Optional

__all__ = ["decode"]


def decode(text: str, name: Optional[str] = None) -> Any:
    """
    A JSONP decoder that reads from text and returns the decoded JSON value.

    Args:
        text (str): A string to read the JSONP payload from.
        name (Optional[str], optional): The expected JSONP callback name. If provided,
            the decoder will verify that the callback name matches. Defaults to None.

    Raises:
        ValueError: malformed JSONP payload when decoding.

    Returns:
        Any: The decoded JSON value.
    """

    data = text.strip()

    lparen = data.find("(")
    rparen = data.rfind(")")
    if lparen == -1 or rparen == -1 or lparen > rparen:
        raise ValueError(
            "Malformed JSONP payload, missing parentheses or incorrect order"
        )

    callback_name = data[:lparen].strip()
    if name is not None and callback_name != name:
        raise ValueError(
            f"Unexpected JSONP callback name: expected '{name}', got '{callback_name}'"
        )

    json_str = data[lparen + 1 : rparen].strip()

    return json.loads(json_str)
