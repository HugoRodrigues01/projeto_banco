import logging
from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models.users import User
from src.settings import Settings

SECRET_KEY = Settings().SECRET_KEY
ALGORITHIM = Settings().ALGORITHIM
ACCESS_TOKEN_EXPIRE_MINUTS = Settings().ACCESS_TOKEN_EXPIRE_MINUTS

logging.basicConfig(level=logging.DEBUG)

pwd_context = PasswordHash.recommended()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_schema),
):
    # Criando uma única variação de erro possível
    credential_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credential.",
        headers={"WWW-Authorization": "Bearer"},
    )

    try:
        logging.info("Entrando no try de get_current_user")
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHIM])
        logging.debug(f"payload: {payload}")
        sub_cpf = payload.get("sub")

        if not sub_cpf:
            raise credential_exception
    except DecodeError:
        raise credential_exception

    user = session.scalar(select(User).where(User.user_cpf == sub_cpf))

    if not user:
        raise credential_exception

    return user


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTS
    )

    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHIM)

    return encoded_jwt


def create_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
