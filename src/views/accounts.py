from pydantic import BaseModel


class AccountView(BaseModel):
    id_conta: int
    agencia_conta: int
    user_cpf: str
    saldo: float
