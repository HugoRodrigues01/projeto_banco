import logging
from http import HTTPStatus

logging.basicConfig(level=logging.DEBUG)


def test_get_account(client, token, account, user):
    response = client.get(
        "/contas", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "accounts": [
            {
                "id_conta": account.id_conta,
                "banco_id": account.banco_id,
                "agencia_conta": account.agencia_conta,
                "user_cpf": user.user_cpf,
                "saldo": account.saldo,
            }
        ]
    }


def test_get_account_with_worng_cpf_user(client, token, user):
    response = client.get(
        "/contas", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        "detail": f"Account with cpf user: {user.user_cpf}, not found."
    }


def test_create_account(client, token, bank2, account):
    response = client.post(
        "/contas",
        json={"agencia_conta": 12344, "banco_id": bank2.id_bank, "saldo": 100},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "agencia_conta": 12344,
        "banco_id": 1,
        "id_conta": 2,
        "saldo": 100.0,
        "user_cpf": "12345678900",
    }


def test_create_account_with_bank_id_not_exists(client, token):
    response = client.post(
        "/contas",
        json={"agencia_conta": 12344, "banco_id": 213, "saldo": 100},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Bank id 213, not found."}


def test_create_account_already_exists_bank(
    client, token, account, bank, user
):
    response = client.post(
        "/contas",
        json={"agencia_conta": 12344, "banco_id": bank.id_bank, "saldo": 100},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        "detail": f"User {user.user_cpf},already \
have an account in the this bank."
    }


def test_get_extract(client, token, bank, transaction, account2):
    response = client.get(
        f"/contas/extrato/{bank.id_bank}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "extract": [
            {
                "conta_destino": account2.id_conta,
                "conta_transmissora": 1,
                "created_at": transaction.created_at.isoformat(),
                "forma_pagamento": "PIX",
                "id_transacao": 1,
                "tipo_trasacao": "TRA",
                "valor": transaction.valor,
            }
        ]
    }


def test_get_extract_with_worgn_id_bank(client, token, transaction):
    response = client.get(
        "/contas/extrato/12",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Account of bank 12 not exists."}
