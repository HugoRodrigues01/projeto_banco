import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ConflictError, NotFoundError
from src.models.accounts import Account
from src.models.banks import Bank
from src.models.transactions import Transactions
from src.schemas.accounts import AccountSchema

logging.basicConfig(level=logging.DEBUG)


class AccountService:
    @classmethod
    async def get_accounts(self, cpf_user: int, session):

        response = await session.scalars(
            select(Account).where(Account.user_cpf == cpf_user)
        )

        responses = response.all()

        if not responses:
            raise NotFoundError(
                detail=f"Account with cpf user: {cpf_user}, not found."
            )

        return responses

    @classmethod
    async def get_extract(self, bank_id, cpf_user, session: AsyncSession):

        agencia = await session.scalar(
            select(Account).where(
                (Account.banco_id == bank_id), (Account.user_cpf == cpf_user)
            )
        )

        # logging.debug(f"Agencia {agencia.id_conta}")

        if not agencia:
            raise NotFoundError(
                detail=f"Account of bank {bank_id} not exists."
            )

        response = await session.scalars(
            select(Transactions).where(
                Transactions.conta_transmissora == agencia.id_conta
            )
        )

        returned = response
        return returned.all()

    @classmethod
    async def create(
        self, account_data: AccountSchema, cpf_user, session: AsyncSession
    ):
        try:
            accounts = await self.get_accounts(cpf_user, session)
            bank_list = [bank.banco_id for bank in accounts]

            if account_data.banco_id not in bank_list:
                raise ConflictError

        except Exception:
            bank_exists = await session.scalar(
                select(Bank).where(Bank.id_bank == account_data.banco_id)
            )
            if not bank_exists:
                raise NotFoundError(
                    detail=f"Bank id {account_data.banco_id}, not found."
                )

            account = Account(
                agencia_conta=account_data.agencia_conta,
                banco_id=account_data.banco_id,
                user_cpf=cpf_user,
                saldo=account_data.saldo,
            )

            session.add(account)
            await session.commit()
            await session.refresh(account)

            return account

        raise ConflictError(
            detail=f"User {cpf_user},already have an account in the this bank."
        )
