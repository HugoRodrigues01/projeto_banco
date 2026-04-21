from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.deps import T_Session, T_User
from src.models.transactions import Transactions, TransactionType
from src.schemas.transactions import TransactionSchema
from src.views.transactions import TransactionView

from . import Account

router = APIRouter(prefix="/transacoes", tags=["transacoes"])


@router.post("/", status_code=HTTPStatus.OK, response_model=TransactionView)
def create_transaction(
    data: TransactionSchema, session: T_Session, current_user: T_User
):
    current_account = session.scalar(
        select(Account).where(Account.user_cpf == current_user.user_cpf)
    )
    new_saldo: float = current_account.saldo

    destination_account = session.scalar(
        select(Account).where(Account.current_account_conta == data.destination_account)
    )

    if not current_account:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User don´t have an account.",
        )

    if not destination_account:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Account {data.destination_account} not found.",
        )

    if data.tipo_transacao == TransactionType.deposito:
        new_saldo += data.valor

    elif data.tipo_transacao == TransactionType.saque:
        if new_saldo >= data.valor:
           new_saldo -= data.valor

        else:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Saldo is not suffer."
            )

    elif data.tipo_transacao == TransactionType.transacao:
        if new_saldo >= data.valor:
            new_saldo = current_account.saldo - data.valor

        else:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Saldo is not suffer."
            )
        
    current_account.saldo = new_saldo
    destination_account.saldo = destination_account.saldo + data.valor
    session.add(current_account)
    session.add(destination_account)

    transaction = Transactions(
        conta_transmissora=current_account.current_account_conta,
        destination_account=data.destination_account,
        forma_pagamento=data.forma_pagamento,
        tipo_trasacao=data.tipo_transacao,
        valor=data.valor,
    )

    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    session.refresh(destination_account)
    session.refresh(current_account)

    return transaction
