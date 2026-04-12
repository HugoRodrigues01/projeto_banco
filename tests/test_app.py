from http import HTTPStatus


def test_will_be_returned_ok_and_hello_world(client):
    response = client.get("/")  # act

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Message": "Hello World"}
