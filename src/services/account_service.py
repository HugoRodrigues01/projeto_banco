from src.models.accounts import Account
from src.models.transactions import Transactions
from src.exceptions import NotFoundError
from sqlalchemy import select
from sqlalchemy.orm import Session



class AccountService:

    def get_one(self, cpf_user: int, session: Session):
        
        response = session.scalar(
            select(Account).where(Account.user_cpf == cpf_user)
        )

        if not response:
            raise NotFoundError(detail=f"User {cpf_user} not found.")

        return response
    
    def get_many(self, session: Session, skip: int = 0, limit: int = 10):
        response = session.scalars(
            select(Account).offset(skip).limit(limit)).all()
        
        return response
    
    def get_extract(self, session: Session, agencia_conta: int):
        response = session.scalars(
            select(Transactions).where(
                Transactions.conta_origem == agencia_conta
            )
        ).all()

        return response