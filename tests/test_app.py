from http import HTTPStatus


def test_will_be_returned_ok_and_hello_world(client):
    response = client.get("/")  # act

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Message": "Hello World"}


def test_get_users(client):
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

    assert user.status_code == HTTPStatus.CREATED
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
