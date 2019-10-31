from jwt import encode, decode
from django.conf import settings

def token_encode(data):
    # read raw data, encode it and return the token
    # raw data should be a dict object
    token_binary = encode(data, settings.SECRET_KEY)
    # convert binary to string
    token_string = token_binary.decode()
    return token_string


def token_decode(token):
    # read token, decode it and return the raw data
    try:
        data = decode(token, settings.SECRET_KEY)
        return data
    except Exception:
        return None