from http import HTTPStatus


def test_create_transaction(client, account, token, account2):
    response = client.post(
        "/transacoes",
        json={
            "conta_destino": account2.id_conta,
            "valor": 10,
            "tipo_transacao": "TRA",
            "forma_pagamento": "PIX",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id_transacao": 1,
        "conta_transmissora": account.id_conta,
        "conta_destino": account2.id_conta,
        "valor": response.json()["valor"],
        "tipo_trasacao": "TRA",
        "forma_pagamento": "PIX",
        "created_at": response.json()["created_at"],
    }


def test_create_transaction_without_origim_account(client, account2, token):
    response = client.post(
        "/transacoes",
        json={
            "conta_destino": account2.id_conta,
            "valor": 10,
            "tipo_transacao": "TRA",
            "forma_pagamento": "PIX",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User don´t have an account."}


def test_create_account_without_destinationo_account(client, token, account):
    response = client.post(
        "/transacoes",
        json={
            "conta_destino": 11,
            "valor": 10,
            "tipo_transacao": "TRA",
            "forma_pagamento": "PIX",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Account 11 not found."}


def test_create_transaction_with_type_deposito(client, token, account):

    saldo_ant = account.saldo
    response = client.post(
        "/transacoes",
        json={
            "conta_destino": account.id_conta,
            "valor": 10,
            "tipo_transacao": "DEP",
            "forma_pagamento": "PIX",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    act_account = client.get(
        "/contas",
        headers={"Authorization": f"Bearer {token}"},
    )

    saldo_act = act_account.json()["accounts"][0]["saldo"]

    assert response.status_code == HTTPStatus.OK
    assert saldo_ant + 10 == saldo_act


def test_create_transaction_with_type_sauqe(client, token, account):

    saldo_ant = account.saldo
    response = client.post(
        "/transacoes",
        json={
            "conta_destino": account.id_conta,
            "valor": 10,
            "tipo_transacao": "SAQ",
            "forma_pagamento": "PIX",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    act_account = client.get(
        "/contas",
        headers={"Authorization": f"Bearer {token}"},
    )

    saldo_act = act_account.json()["accounts"][0]["saldo"]

    assert response.status_code == HTTPStatus.OK
    assert saldo_ant - 10 == saldo_act


def test_create_transaction_with_type_sauqe_withou_saldo(
    client, token, account
):

    response = client.post(
        "/transacoes",
        json={
            "conta_destino": account.id_conta,
            "valor": account.saldo + 10,
            "tipo_transacao": "SAQ",
            "forma_pagamento": "PIX",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Saldo is not suffer."}


def test_create_transaction_with_type_transaction_withou_saldo(
    client, token, account, account2
):

    response = client.post(
        "/transacoes",
        json={
            "conta_destino": account2.id_conta,
            "valor": account.saldo + 10,
            "tipo_transacao": "TRA",
            "forma_pagamento": "PIX",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Saldo is not suffer."}
