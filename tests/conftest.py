from datetime import date

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

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


@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        engine = create_async_engine(postgres.get_connection_url())

        yield engine


@pytest_asyncio.fixture
async def session(engine):

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def bank(session):
    bank = Bank(bank_name="BancoTeste S.A")

    session.add(bank)
    await session.commit()
    await session.refresh(bank)

    return bank


@pytest_asyncio.fixture
async def bank2(session):
    bank = Bank(bank_name="BancoTeste2 S.A")

    session.add(bank)
    await session.commit()
    await session.refresh(bank)

    return bank


@pytest_asyncio.fixture
async def user(session):
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
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def account(user, bank, session):
    account_user = Account(
        agencia_conta=12345,
        banco_id=bank.id_bank,
        user_cpf=user.user_cpf,
        saldo=100,
    )

    session.add(account_user)
    await session.commit()
    await session.refresh(account_user)

    return account_user


@pytest_asyncio.fixture
async def user2(session):
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
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def account2(user2, bank, session):
    account_user2 = Account(
        agencia_conta=56789,
        banco_id=bank.id_bank,
        user_cpf=user2.user_cpf,
        saldo=100,
    )

    session.add(account_user2)
    await session.commit()
    await session.refresh(account_user2)

    return account_user2


@pytest_asyncio.fixture
async def transaction(account, account2, session):
    transaction = Transactions(
        conta_transmissora=account.id_conta,
        conta_destino=account2.id_conta,
        valor=10,
        tipo_trasacao=TransactionType.transacao,
        forma_pagamento=PaymentType.pix,
    )

    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)

    return transaction


@pytest_asyncio.fixture
async def transaction2(account, account2, session):
    transaction = Transactions(
        conta_transmissora=account.agencia_conta,
        conta_destino=account2.agencia_conta,
        valor=10,
        tipo_trasacao=TransactionType.transacao,
        forma_pagamento=PaymentType.pix,
    )

    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)

    return transaction


@pytest.fixture
def token(user):
    token_access = create_access_token({"sub": user.user_cpf})
    return token_access
