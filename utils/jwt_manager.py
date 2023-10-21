from fastapi import Request
from fastapi.security import HTTPBearer
from jwt import decode, encode


def create_token(data: dict):
    token: str = encode(payload=data, key="my_secrete_key", algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    data: dict = decode(token, key="my_secrete_key", algorithms=["HS256"])
    return data


async def get_user_id(req: Request):
    auth = await HTTPBearer().__call__(req)
    credentials = validate_token(auth.credentials)
    return credentials["user_id"]
