"""
Simple Base64 encoding library.

Backporting from the script, there's no decoder needed.
"""

from io import StringIO

__all__ = ["encode"]
BASE64_ENCODE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def encode(item: str) -> str:
    """
    Encode a string into Base64 format.

    Args:
        item (str): The string to encode.

    Returns:
        str: The Base64 encoded string.
    """

    result = StringIO()

    index = 0
    while index < len(item):
        c1 = ord(item[index]) & 0xFF
        index += 1
        if index == len(item):
            result.write(BASE64_ENCODE_CHARS[c1 >> 2])
            result.write(BASE64_ENCODE_CHARS[(c1 & 0x3) << 4])
            result.write("==")
            break
        c2 = ord(item[index]) & 0xFF
        index += 1
        if index == len(item):
            result.write(BASE64_ENCODE_CHARS[c1 >> 2])
            result.write(BASE64_ENCODE_CHARS[((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4)])
            result.write(BASE64_ENCODE_CHARS[(c2 & 0xF) << 2])
            result.write("=")
            break
        c3 = ord(item[index]) & 0xFF
        index += 1
        result.write(BASE64_ENCODE_CHARS[c1 >> 2])
        result.write(BASE64_ENCODE_CHARS[((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4)])
        result.write(BASE64_ENCODE_CHARS[((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6)])
        result.write(BASE64_ENCODE_CHARS[c3 & 0x3F])

    return result.getvalue()
