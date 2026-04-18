from http import HTTPStatus


def test_token_with_worng_cpf(client, user):
    request = client.post(
        "/token", data={"username": "12345678932", "password": "teste123"}
    )

    assert request.json() == {"detail": "Iconrrect cpf or password"}
    assert request.status_code == HTTPStatus.UNAUTHORIZED


def test_token_with_worng_password(client, user):
    request = client.post(
        "/token",
        data={"username": "12345678900", "password": "senhaerrada"},
    )

    assert request.json() == {"detail": "Iconrrect cpf or password"}
    assert request.status_code == HTTPStatus.UNAUTHORIZED


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.user_cpf, "password": "teste123"},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token
