from pydantic import BaseModel


class AccountSchema(BaseModel):
    agencia_conta: int
    banco_id: int
    saldo: float = 0
