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

@router.get("/", status_code=HTTPStatus.OK, response_model=AccountListView)
def get_account(user: T_User, session: T_Session):
    account = account_service.get_accounts(user.user_cpf, session)
   
    return {"accounts": account}


@router.get("/list", response_model=AccountListView)
def get_accounts(session: T_Session, skip: int = 0, limit: int = 10):
    accounts = session.scalars(
            select(Account).offset(skip).limit(limit)).all()

    return {"accounts": accounts}


@router.get("/extrato/{banco_id}")
def get_extract(banco_id: int, session: T_Session, current_user: T_User):
    extract = account_service.get_extract(banco_id, current_user.user_cpf, session)

    return {"extact": extract}


@router.post("/", status_code=HTTPStatus.CREATED, response_model=AccountView)
def create_account(
    account_data: AccountSchema, session: T_Session, current_user: T_User
):
    account = account_service.create(account_data, current_user.user_cpf, session)

    return account

@router.post("/")
def enable_disable_account():
    pass
