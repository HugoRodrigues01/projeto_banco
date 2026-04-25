from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from src.app import app
from src.database import get_session
from src.models.accounts import Account
from src.models.banks import Bank
from src.models.registry import table_registry
from src.models.transactions import PaymentType, Transactions, TransactionType
from src.models.users import SexoCliente, User
from src.security import create_access_token, create_password_hash

# class TransactionFactory(factory.Factory):
#     class Meta:
#         model = Transactions

#     tranmissor_account = factory.Sequence(lambda n: n * 1000)
#     conta_destino = None
#     valor


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def bank(session):
    bank = Bank(bank_name="BancoTeste S.A")

    session.add(bank)
    session.commit()
    session.refresh(bank)

    return bank


@pytest.fixture
def bank2(session):
    bank = Bank(bank_name="BancoTeste2 S.A")

    session.add(bank)
    session.commit()
    session.refresh(bank)

    return bank


@pytest.fixture
def user(session):
    user = User(
        username="naoexiste",
        phone_number=98981330984,
        user_email="naoexiste@gmail.com",
        user_cpf="12345678900",
        data_nascimento=date(2004, 2, 14),
        sexo_cliente=SexoCliente.masculino,
        password=create_password_hash("teste123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def account(user, bank, session):
    account_user = Account(
        agencia_conta=12345,
        banco_id=bank.id_bank,
        user_cpf=user.user_cpf,
        saldo=100,
    )

    session.add(account_user)
    session.commit()
    session.refresh(account_user)

    return account_user


@pytest.fixture
def user2(session):
    user = User(
        username="naoexiste2",
        phone_number=98981330984,
        user_email="naoexiste2@gmail.com",
        user_cpf="12345632900",
        data_nascimento=date(2000, 12, 21),
        sexo_cliente=SexoCliente.nao_informado,
        password=create_password_hash("teste123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def account2(user2, bank, session):
    account_user2 = Account(
        agencia_conta=56789,
        banco_id=bank.id_bank,
        user_cpf=user2.user_cpf,
        saldo=100,
    )

    session.add(account_user2)
    session.commit()
    session.refresh(account_user2)

    return account_user2


@pytest.fixture
def transaction(account, account2, session):
    transaction = Transactions(
        conta_transmissora=account.agencia_conta,
        conta_destino=account2.agencia_conta,
        valor=10,
        tipo_trasacao=TransactionType.transacao,
        forma_pagamento=PaymentType.pix,
    )

    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return transaction


@pytest.fixture
def transaction2(account, account2, session):
    transaction = Transactions(
        conta_transmissora=account.agencia_conta,
        conta_destino=account2.agencia_conta,
        valor=10,
        tipo_trasacao=TransactionType.transacao,
        forma_pagamento=PaymentType.pix,
    )

    session.add(transaction)
    session.commit()
    session.refresh(transaction)


@pytest.fixture
def token(user):
    token_access = create_access_token({"sub": user.user_cpf})
    return token_access
