from datetime import UTC, date, datetime

from pydantic import BaseModel

from src.models.users import SexoCliente


class UserSchema(BaseModel):
    username: str
    user_cpf: str
    phone_number: int
    user_email: str
    data_nascimento: date
    sexo_cliente: SexoCliente
    password: str
    created_at: datetime = datetime.now(UTC)
    updated_at: datetime = datetime.now(UTC)


class UserUpdateSchema(BaseModel):
    username: str
    phone_number: int
    user_email: str
    password: str
    data_nascimento: date
    sexo_cliente: SexoCliente
    password: str
