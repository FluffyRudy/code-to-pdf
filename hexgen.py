import secrets


def get_random_hex(length: int) -> str:
    if not isinstance(length, int):
        raise TypeError("Expected length as integer")
    random_byte = secrets.token_bytes(length)
    return random_byte.hex()
