from datetime import date

from pydantic import BaseModel

from src.models.users import SexoCliente


class UserView(BaseModel):
    user_id: int
    user_cpf: str
    username: str
    user_email: str
    data_nascimento: date
    sexo_cliente: SexoCliente


class UserListView(BaseModel):
    users: list[UserView]
