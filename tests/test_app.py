from http import HTTPStatus


def test_will_be_returned_ok_and_hello_world(client):
    response = client.get("/")  # act

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Message": "Hello World"}


def test_get_one_user(client, user):
    result = client.get(
        "/usuarios/1",
    )

    assert result.status_code == HTTPStatus.OK
    assert result.json() == {
        "user_id": 1,
        "username": "naoexiste",
        "user_email": "naoexiste@gmail.com",
    }


def test_check_if_user_exists(client, user):
    result = client.get("/usuarios/12")

    assert result.status_code == HTTPStatus.NOT_FOUND
    assert result.json() == {"detail": "User id not exists."}


def test_delete_user(client, user):
    response = client.delete("/usuarios/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "user_id": 1,
        "username": "naoexiste",
        "user_email": "naoexiste@gmail.com",
    }


def test_delete_not_found_user(client):

    response = client.delete("/usuarios/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User do not exists."}


def test_update_user(client, user):
    response = client.put(
        "/usuarios/1",
        json={
            "username": "trocar",
            "phone_number": 98981330984,
            "user_email": "naoexiste@gmail.com",
            "password": "teste123",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "user_id": 1,
        "username": "trocar",
        "user_email": "naoexiste@gmail.com",
    }


def test_update_not_found_user(client):
    response = client.put(
        "/usuarios/1",
        json={
            "username": "trocar",
            "phone_number": 98981330984,
            "user_email": "naoexiste@gmail.com",
            "password": "teste123",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User do not exists."}


def test_get_many_users(client):
    users = client.get("/usuarios/")

    assert users.status_code == HTTPStatus.OK


def test_create_user(client):
    user = client.post(
        "/usuarios/",
        json={
            "username": "naoexiste",
            "phone_number": 98981330984,
            "user_email": "naoexiste@gmail.com",
            "password": "teste123",
        },
    )

    assert user.status_code == HTTPStatus.CREATED
    assert user.json() == {
        "user_id": 1,
        "username": "naoexiste",
        "user_email": "naoexiste@gmail.com",
    }


def test_check_if_username_already_exists(client, user):

    user2 = client.post(
        "/usuarios/",
        json={
            "username": "naoexiste",
            "phone_number": 98981330984,
            "user_email": "naoexiste@gmail.com",
            "password": "teste123",
        },
    )

    assert user2.status_code == HTTPStatus.CONFLICT
    assert user2.json() == {"detail": "Username already exists."}


def test_check_if_user_email_already_exists(client):
    user = client.post(
        "/usuarios/",
        json={
            "username": "naoexiste",
            "phone_number": 98981330984,
            "user_email": "naoexiste@gmail.com",
            "password": "teste123",
        },
    )

    user2 = client.post(
        "/usuarios/",
        json={
            "username": "newname",
            "phone_number": 98981330984,
            "user_email": "naoexiste@gmail.com",
            "password": "teste123",
        },
    )

    assert user.status_code == HTTPStatus.CREATED
    assert user2.status_code == HTTPStatus.CONFLICT
    assert user2.json() == {"detail": "Use email already exists."}


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.user_email, "password": "teste123"},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token
