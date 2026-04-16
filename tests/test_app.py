def test_hello_world(client):
    request = client.get("/")

    assert request.json() == {"Message": "Hello World"}
