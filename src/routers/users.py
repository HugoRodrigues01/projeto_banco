from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models.users import User
from src.schemas.users import UserSchema, UserUpdateSchema
from src.security import create_password_hash, get_current_user
from src.views.users import UserListView, UserView

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/", status_code=HTTPStatus.OK, response_model=UserListView)
def get_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@router.get("/{id}", status_code=HTTPStatus.OK, response_model=UserView)
def get_user(id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.user_id == id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User id not exists."
        )

    return user


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserView)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.user_cpf == user.user_cpf)
            | (User.user_email == user.user_email)
            | (User.username == user.username)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists.",
            )
        if db_user.user_cpf == user.user_cpf:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Use cpf already exists.",
            )
        if db_user.user_email == user.user_email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Use email already exists.",
            )

    db_user = User(
        username=user.username,
        user_email=user.user_email,
        user_cpf=user.user_cpf,
        data_nascimento=user.data_nascimento,
        sexo_cliente=user.sexo_cliente,
        phone_number=user.phone_number,
        password=create_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.put("/{id}", status_code=HTTPStatus.CREATED, response_model=UserView)
def update_user(
    id: int,
    new_user: UserUpdateSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.user_id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )

    current_user.username = new_user.username
    current_user.user_email = (
        new_user.user_email or current_user.user.user_email
    )
    current_user.password = (
        create_password_hash(new_user.password) or current_user.password
    )
    current_user.phone_number = (
        new_user.phone_number or current_user.phone_number
    )
    current_user.sexo_cliente = (
        new_user.sexo_cliente or current_user.sexo_cliente
    )

    current_user.data_nascimento = (
        new_user.data_nascimento or current_user.data_nascimento
    )

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete("/{id}", status_code=HTTPStatus.OK, response_model=UserView)
def delete_user(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.user_id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permissions"
        )

    session.delete(current_user)
    session.commit()

    return current_user
