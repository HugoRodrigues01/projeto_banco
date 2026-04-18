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
        "data_nascimento": "2004-02-14",
        "sexo_cliente": "M",
        "user_cpf": "12345678900"
    }


def test_check_if_user_exists(client, user):
    result = client.get("/usuarios/12")

    assert result.status_code == HTTPStatus.NOT_FOUND
    assert result.json() == {"detail": "User id not exists."}


def test_delete_user(client, token):
    response = client.delete(
        "/usuarios/1", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "user_id": 1,
        "username": "naoexiste",
        "user_email": "naoexiste@gmail.com",
        "data_nascimento": "2004-02-14",
        "sexo_cliente": "M",
        'user_cpf': '12345678900'
    }


def test_delete_not_found_user(client):
    response = client.delete(
        "/usuarios/1", headers={"Authorization": "Bearer "}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credential."}


def test_delete_user_without_permission(client, token):
    response = client.delete(
        "/usuarios/100", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


def test_update_user(client, token):
    response = client.put(
        "/usuarios/1",
        json={
            "username": "hugoupdate",
            "phone_number": 12345612378,
            "user_email": "update@gmail.com",
            "password": "teste123",
            "data_nascimento": "2004-02-14",
            "sexo_cliente": "F"
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "user_id": 1,
        "user_cpf": "12345678900",
        "username": "hugoupdate",
        "user_email": "update@gmail.com",
        "data_nascimento": "2004-02-14",
        "sexo_cliente": "F",
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
        headers={"Authorization": "Bearer "},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credential."}


def test_update_user_without_permission(client, token):
    response = client.put(
        "/usuarios/1000",
        json={
            "username": "hugoupdate",
            "phone_number": 12345612378,
            "user_email": "update@gmail.com",
            "password": "teste123",
            "data_nascimento": "2004-02-14",
            "sexo_cliente": "F"
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


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
            "user_cpf": "12345612378",
            "data_nascimento": "2004-02-14",
            "sexo_cliente": "M",
        },
    )

    assert user.status_code == HTTPStatus.CREATED
    assert user.json() == {
        "user_id": 1,
        "data_nascimento": "2004-02-14",
        "sexo_cliente": "M",
        "username": "naoexiste",
        "user_email": "naoexiste@gmail.com",
        "user_cpf": "12345612378"
    }


def test_check_if_username_already_exists(client, user):
    user2 = client.post(
        "/usuarios/",
        json={
            "username": "naoexiste",
            "phone_number": 98981330984,
            "user_email": "naoexiste@gmail.com",
            "password": "teste123",
            "user_cpf": "12345612378",
            "data_nascimento": "2004-02-14",
            "sexo_cliente": "M",
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
            "user_cpf": "12345678900",
            "data_nascimento": "2004-02-14",
            "sexo_cliente": "M",
        },
    )

    user2 = client.post(
        "/usuarios/",
        json={
            "username": "newname",
            "phone_number": 98981330984,
            "user_email": "naoexiste@gmail.com",
            "password": "teste123",
            "user_cpf": "1723289129",
            "data_nascimento": "2004-02-14",
            "sexo_cliente": "M",
        },
    )

    assert user.status_code == HTTPStatus.CREATED
    assert user2.status_code == HTTPStatus.CONFLICT
    assert user2.json() == {"detail": "Use email already exists."}
