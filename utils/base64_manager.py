import base64


def base64_decode(value: str):
    convertbytes = value.encode("ascii")
    convertedbytes = base64.b64decode(convertbytes)
    decodedsample = convertedbytes.decode("ascii")
    return decodedsample
