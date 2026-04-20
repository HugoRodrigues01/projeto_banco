import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from src.deps import T_Session
from src.models.users import User
from src.schemas.token import TokenSchema
from src.security import create_access_token, verify_password

router = APIRouter(prefix="/token", tags=["token"])


logging.basicConfig(level=logging.DEBUG)


@router.post("/", response_model=TokenSchema)
def login_for_access_token(
    session: T_Session, form_data: OAuth2PasswordRequestForm = Depends()
):
    logging.debug("Estou no login_access_token")
    cpf = str(form_data.username)
    user = session.scalar(select(User).where(User.user_cpf == cpf))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Iconrrect cpf or password",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Iconrrect cpf or password",
        )

    access_token = create_access_token({"sub": user.user_cpf})
    return {"access_token": access_token, "token_type": "bearer"}
