from http import HTTPStatus


def test_token_with_worng_email(client, user):
    request = client.post(
        "/token", data={"username": "@gmail.com", "password": "string"}
    )

    assert request.json() == {"detail": "Iconrrect email or password"}
    assert request.status_code == HTTPStatus.UNAUTHORIZED


def test_token_with_worng_password(client, user):
    request = client.post(
        "/token",
        data={"username": "naoexiste@gmail.com", "password": "senhaerrada"},
    )

    assert request.json() == {"detail": "Iconrrect email or password"}
    assert request.status_code == HTTPStatus.UNAUTHORIZED


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.user_email, "password": "teste123"},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token
