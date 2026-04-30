from datetime import date

import pytest
from sqlalchemy import select

from src.models.users import SexoCliente, User


@pytest.mark.asyncio
async def test_create_user(session):
    new_user = User(
        username="Hugo rodrigues",
        phone_number=98981352143,
        user_email="teste@gmail.com",
        password="passwordtest123",
        user_cpf="89343583239",
        data_nascimento=date(2004, 2, 14),
        sexo_cliente=SexoCliente.masculino,
    )

    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(User).where(User.username == "Hugo rodrigues")
    )

    assert user.username == "Hugo rodrigues"
