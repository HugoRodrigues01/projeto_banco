from typing import TYPE_CHECKING, List
from datetime import date, datetime
from enum import Enum

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.registry import table_registry

if TYPE_CHECKING:
    from src.models.acounts import Acount

class SexoCliente(Enum):
    masculino = "M"
    feminino = "F"
    nao_informado = "NI"


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "table_user"

    user_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_cpf: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True)
    data_nascimento: Mapped[date] = mapped_column(nullable=False)
    phone_number: Mapped[int]
    user_email: Mapped[str] = mapped_column(unique=True)
    sexo_cliente: Mapped[SexoCliente]
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )

    acount: Mapped[List["Acount"]] = relationship("user")