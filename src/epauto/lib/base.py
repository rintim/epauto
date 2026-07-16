"""
Simple Base64 encoding library.

Compatible with the original script's base64 encoding logic, but use Python's built-in base64 module for simplicity and reliability.
"""

import base64

__all__ = ["encode"]


def encode(item: str) -> str:
    """
    Encode a string into Base64 format using the original script's byte semantics.

    Args:
        item (str): The string to encode.

    Returns:
        str: The Base64 encoded string.
    """

    payload = bytes(ord(char) & 0xFF for char in item)
    return base64.b64encode(payload).decode("ascii")
