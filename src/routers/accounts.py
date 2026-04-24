from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.deps import T_Session, T_User
from src.schemas.accounts import AccountSchema
from src.views.accounts import AccountListView, AccountView
from src.services.account_service import AccountService

from . import Account, Transactions

router = APIRouter(prefix="/contas", tags=["contas"])
account_service = AccountService()

@router.get("/", status_code=HTTPStatus.OK, response_model=AccountView)
def get_account(user: T_User, session: T_Session):
    account = account_service.get_one(user.user_cpf, session)
    print("Current account: ", account)
    return account


@router.get("/list", response_model=AccountListView)
def get_accounts(session: T_Session, skip: int = 0, limit: int = 10):
    accounts = account_service.get_many(session=session, skip=skip, limit=limit)


    return {"accounts": accounts}


@router.get("/extrato")
def get_extract(session: T_Session, current_user: T_User):
    current_account = account_service.get_one(current_user.user_cpf, session)
    

    extract = account_service.get_extract(session, agencia_conta=current_account.agencia_conta)

    return {"extact": extract}


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
def enable_disable_account():
    pass
