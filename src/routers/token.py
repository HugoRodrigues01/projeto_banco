from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.users import User
from src.schemas.token import TokenSchema
from src.security import create_access_token, get_session, verify_password

router = APIRouter(prefix="/token", tags=["token"])


@router.post("/", response_model=TokenSchema)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):

    user = session.scalar(
        select(User).where(User.user_email == form_data.username)
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Iconrrect email or password",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Iconrrect email or password",
        )

    access_token = create_access_token({"sub": user.user_email})
    return {"access_token": access_token, "token_type": "bearer"}
