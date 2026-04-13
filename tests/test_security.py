from jwt import decode

from src.security import (
    SECRET_KEY,
    create_access_token,
    create_password_hash,
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
