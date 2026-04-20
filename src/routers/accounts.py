from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.deps import T_Session, T_User
from src.models.accounts import Account
from src.schemas.accounts import AccountSchema
from src.views.accounts import AccountView

router = APIRouter(prefix="/contas", tags=["contas"])


@router.get("/", status_code=HTTPStatus.OK, response_model=AccountView)
def get_account(session: T_Session, user: T_User):
    account = session.scalar(
        select(Account).where(Account.user_cpf == user.user_cpf)
    )

    if not account:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User don´t hava an account."
        )
    
    return account


@router.post("/", status_code=HTTPStatus.CREATED, response_model=AccountView)
def create_account(
    account_data: AccountSchema, session: T_Session, current_user: T_User
):
    account = session.scalar(
        select(Account).where(
            Account.agencia_conta == account_data.agencia_conta
        )
    )

    if account:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"Account {account.agencia_conta} already exists.",
        )

    account = Account(
        agencia_conta=account_data.agencia_conta,
        banco_id=account_data.banco_id,
        user_cpf=str(current_user.user_cpf),
        saldo=account_data.saldo,
    )

    session.add(account)
    session.commit()
    session.refresh(account)

    return account


@router.post("/")
def enable_disable_account(): pass