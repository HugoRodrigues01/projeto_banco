from http import HTTPStatus

from fastapi import APIRouter

from src.deps import T_Session, T_User
from src.schemas.accounts import AccountSchema
from src.services.account_service import AccountService
from src.views.accounts import AccountListView, AccountView

router = APIRouter(prefix="/contas", tags=["contas"])
account_service = AccountService()


@router.get("/", status_code=HTTPStatus.OK, response_model=AccountListView)
def get_account(user: T_User, session: T_Session):
    account = account_service.get_accounts(user.user_cpf, session)

    return {"accounts": account}


@router.get("/extrato/{banco_id}")
def get_extract(banco_id: int, session: T_Session, current_user: T_User):
    extract = account_service.get_extract(
        banco_id, current_user.user_cpf, session
    )

    return {"extract": extract}


@router.post("/", status_code=HTTPStatus.CREATED, response_model=AccountView)
def create_account(
    account_data: AccountSchema, session: T_Session, current_user: T_User
):
    account = account_service.create(
        account_data, current_user.user_cpf, session
    )

    return account


@router.post("/")
def enable_disable_account():
    pass
