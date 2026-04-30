import logging
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.deps import T_Session, T_User
from src.models.transactions import Transactions, TransactionType
from src.schemas.transactions import TransactionSchema
from src.views.transactions import TransactionView

from . import Account

logging.basicConfig(level=logging.DEBUG)

router = APIRouter(prefix="/transacoes", tags=["transacoes"])


@router.post("/", status_code=HTTPStatus.OK, response_model=TransactionView)
async def create_transaction(
    data: TransactionSchema, session: T_Session, current_user: T_User
):
    current_account = await session.scalar(
        select(Account).where(Account.user_cpf == current_user.user_cpf)
    )

    destination_account = await session.scalar(
        select(Account).where(Account.id_conta == data.conta_destino)
    )

    if not current_account:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User don´t have an account.",
        )

    if not destination_account:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Account {data.conta_destino} not found.",
        )

    new_saldo: float = current_account.saldo

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
        destination_account.saldo += data.valor
        session.add(destination_account)

    current_account.saldo = new_saldo

    session.add(current_account)

    transaction = Transactions(
        conta_transmissora=current_account.id_conta,
        conta_destino=data.conta_destino,
        forma_pagamento=data.forma_pagamento,
        tipo_trasacao=data.tipo_transacao,
        valor=data.valor,
    )

    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    await session.refresh(destination_account)
    await session.refresh(current_account)

    return transaction
