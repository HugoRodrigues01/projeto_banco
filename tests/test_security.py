from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from src.security import (
    SECRET_KEY,
    create_access_token,
    create_password_hash,
    get_current_user,
    verify_password,
)


def test_create_access_token():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=["HS256"])

    assert decoded["test"] == data["test"]
    assert "exp" in decoded


def test_create_an_hash_fo_password_and_decode():
    password = "test123"
    hashed_password = create_password_hash(password)

    assert verify_password(password, hashed_password)


def test_get_current_user_with_not_sub_email(session):
    token_new = create_access_token({})
    with pytest.raises(HTTPException) as exc:
        get_current_user(session=session, token=token_new)

    assert exc.value.status_code == HTTPStatus.UNAUTHORIZED


def test_get_current_user_with_not_found_user(session, user):
    token_new = create_access_token({"sub": "teste"})

    with pytest.raises(HTTPException) as exc:
        get_current_user(session=session, token=token_new)

    assert exc.value.status_code == HTTPStatus.UNAUTHORIZED
