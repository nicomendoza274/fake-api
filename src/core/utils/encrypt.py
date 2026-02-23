import base64
import hashlib
from datetime import datetime, timedelta

import pytz
from jwt import decode, encode

from src.core.classes.settings import settings


def encrypt_string(hash_string: str) -> str:
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def base64_decode(value: str) -> str:
    convert_bytes = value.encode("ascii")
    converted_bytes = base64.b64decode(convert_bytes)
    decoded_sample = converted_bytes.decode("ascii")
    return decoded_sample


def create_token(
    data: dict,
    expired_time: int = settings.TOKEN_EXPIRE_DAYS,
) -> tuple[str, datetime]:
    to_encode = data.copy()
    token_expires = datetime.now(pytz.utc) + timedelta(days=expired_time)
    to_encode.update({"exp": token_expires})
    token: str = encode(
        payload=to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )
    return token, token_expires


def validate_token(token: str) -> dict:
    data: dict = decode(
        token,
        key=settings.SECRET_KEY,
        algorithms=[settings.TOKEN_ALGORITHM],
    )
    return data
