import base64
import hashlib


def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


def base64_decode(value: str):
    convertbytes = value.encode("ascii")
    convertedbytes = base64.b64decode(convertbytes)
    decodedsample = convertedbytes.decode("ascii")
    return decodedsample
