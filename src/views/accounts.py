from typing import List

from pydantic import BaseModel


class AccountView(BaseModel):
    id_conta: int
    banco_id: int
    agencia_conta: int
    user_cpf: str
    saldo: float


class AccountListView(BaseModel):
    accounts: List[AccountView]
