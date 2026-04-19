from http import HTTPStatus


def test_get_bank(client, bank):
    bank_one = client.get("/bancos/1")

    assert bank_one.status_code == HTTPStatus.OK
    assert bank_one.json() == {"id_bank": 1, "bank_name": "BancoTeste S.A"}


def test_get_bank_if_not_exists(client):
    bank_one = client.get("/bancos/1")

    assert bank_one.status_code == HTTPStatus.NOT_FOUND
    assert bank_one.json() == {"detail": "Bank with id 1 not found."}


def test_get_banks(client, bank):
    banks = client.get("/bancos")

    assert banks.status_code == HTTPStatus.OK
    assert banks.json() == {
        "banks": [{"id_bank": 1, "bank_name": "BancoTeste S.A"}]
    }


def test_create_bank(client):
    bank = client.post("/bancos", json={"bank_name": "TesteBanco S.A"})

    assert bank.status_code == HTTPStatus.CREATED
    assert bank.json() == {"id_bank": 1, "bank_name": "TesteBanco S.A"}


def test_create_bank_already_exists(client, bank):
    bank2 = client.post("/bancos", json={"bank_name": "BancoTeste S.A"})

    assert bank2.status_code == HTTPStatus.CONFLICT
    assert bank2.json() == {"detail": "Bank name already exists."}
