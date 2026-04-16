import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from src.app import app
from src.database import get_session
from src.models.users import User, table_registry
from src.security import create_access_token, create_password_hash


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
def user(session):
    user = User(
        username="naoexiste",
        phone_number=98981330984,
        user_email="naoexiste@gmail.com",
        password=create_password_hash("teste123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def user2(session):
    user = User(
        username="naoexiste2",
        phone_number=98981330984,
        user_email="naoexiste2@gmail.com",
        password=create_password_hash("teste123"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token(user):
    token_access = create_access_token({"sub": user.user_email})
    return token_access
