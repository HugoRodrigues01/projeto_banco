from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.registry import table_registry

if TYPE_CHECKING:
    from src.models.accounts import Account


class TransactionType(Enum):
    deposito = "DEP"
    saque = "SAQ"
    transacao = "TRA"


class PaymentType(Enum):
    debito = "DEB"
    credito = "CRE"
    dinheiro = "DIN"
    pix = "PIX"


@table_registry.mapped_as_dataclass
class Transactions:
    __tablename__ = "table_transacoes"

    id_transacao: Mapped[int] = mapped_column(init=False, primary_key=True)
    conta_transmissora: Mapped[int] = mapped_column(
        ForeignKey("table_conta.id_conta")
    )
    conta_destino: Mapped[int] = mapped_column(nullable=False)
    valor: Mapped[float] = mapped_column(nullable=False)
    tipo_trasacao: Mapped[TransactionType]
    forma_pagamento: Mapped[PaymentType]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )

    conta_origem: Mapped["Account"] = relationship(
        "Account",
        foreign_keys=[conta_transmissora],
        back_populates="transacoes_enviadas",
        init=False,
    )
