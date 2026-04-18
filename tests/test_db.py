from datetime import date

from sqlalchemy import select

from src.models.users import SexoCliente, User


def test_create_user(session):
    new_user = User(
        username="Hugo rodrigues",
        phone_number=98981352143,
        user_email="teste@gmail.com",
        password="passwordtest123",
        user_cpf=89343583239,
        data_nascimento=date(2004, 2, 14),
        sexo_cliente=SexoCliente.masculino,
    )

    session.add(new_user)
    session.commit()

    user = session.scalar(
        select(User).where(User.username == "Hugo rodrigues")
    )

    assert user.username == "Hugo rodrigues"
