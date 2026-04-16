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
