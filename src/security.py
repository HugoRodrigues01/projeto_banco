from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode

SECRET_KEY = ""
ALGORITHIM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTS = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTS
    )

    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHIM)

    return encoded_jwt
