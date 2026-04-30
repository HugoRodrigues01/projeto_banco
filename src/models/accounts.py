from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.registry import table_registry

if TYPE_CHECKING:
    from src.models.banks import Bank
    from src.models.transactions import Transactions
    from src.models.users import User


@table_registry.mapped_as_dataclass
class Account:
    __tablename__ = "table_conta"

    id_conta: Mapped[int] = mapped_column(init=False, primary_key=True)
    agencia_conta: Mapped[int] = mapped_column(nullable=False)
    banco_id: Mapped[int] = mapped_column(ForeignKey("table_banco.id_bank"))
    user_cpf: Mapped[str] = mapped_column(ForeignKey("table_user.user_cpf"))
    saldo: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )

    # relationship
    bank: Mapped["Bank"] = relationship(
        "Bank", back_populates="account", init=False
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="account", init=False
    )

    # transmissor_account: Mapped[list["Transactions"]] = relationship(
    #     back_populates="transmissor_account_rel", init=False
    # )

    # destination_account: Mapped[list["Transactions"]] = relationship(
    #     back_populates="destination_account_rel", init=False
    # )

    transacoes_enviadas: Mapped[list["Transactions"]] = relationship(
        "Transactions",
        back_populates="conta_origem",
        # foreign_keys=[Transactions.conta_transmissora],
        init=False,
    )
