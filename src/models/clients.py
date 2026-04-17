import enum
from datetime import datetime
from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.models import table_registry


class SexoCliente(enum.Enum):
    masculino = "M"
    feminino = "F"
    nao_informado = "NI"


@table_registry.mapped_as_dataclass
class Client:
    __tablename__ = "table_client"

    cpf_cliente: Mapped[int] = mapped_column(primary_key=True)
    nome_cliente: Mapped[str] = mapped_column(nullable=False)
    data_nascimento: Mapped[date] = mapped_column(nullable=False)
    telefone: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    sexo_cliente: Mapped[SexoCliente]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )
