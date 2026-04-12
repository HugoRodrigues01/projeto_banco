from sqlalchemy import select

from src.models.users import User


def test_create_user(session):
    new_user = User(
        username="Hugo rodrigues",
        phone_number=98981352143,
        user_email="teste@gmail.com",
        password="passwordtest123",
    )

    session.add(new_user)
    session.commit()

    user = session.scalar(
        select(User).where(User.username == "Hugo rodrigues")
    )

    assert user.username == "Hugo rodrigues"
