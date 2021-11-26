import jwt
from typing import Dict
from decouple import config
import time
import logging

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(id: str, role: str) -> Dict[str, str]:
    payload = {
        "id": id,
        "role": role,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[jwt.get_unverified_header(token)['alg']])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception as e:
        logging.error(str(e))
        return {}
