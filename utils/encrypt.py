import base64
import hashlib

from jwt import decode, encode

from utils.settings import Settings

settings = Settings()

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def base64_decode(value: str):
    convertbytes = value.encode("ascii")
    convertedbytes = base64.b64decode(convertbytes)
    decodedsample = convertedbytes.decode("ascii")
    return decodedsample

def create_token(data: dict):
    token: str = encode(payload=data, key=settings.MY_SECRET_KEY, algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key=settings.MY_SECRET_KEY, algorithms=["HS256"])
    return data

# def expire_token(data:dict):
#     to_encode = data.copy()
#     token_expires = timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
#     expire = datetime.utcnow() + token_expires
#     to_encode.update({'exp':expire})
#     return to_encode
