from typing import TYPE_CHECKING
from src.models.registry import table_registry

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
from datetime import datetime


if TYPE_CHECKING:
    from src.models.banks import Bank
    from src.models.users import User


@table_registry.mapped_as_dataclass
class Acount:
    __tablename__ = "table_conta"

    id_conta: Mapped[int] = mapped_column(init=False, primary_key=True)
    agencia_conta: Mapped[int] = mapped_column(nullable=False, unique=True)
    banco_id: Mapped[int] = mapped_column(ForeignKey("table_banco.id_bank"))
    id_usuario: Mapped[int] = mapped_column(ForeignKey("table_user.user_id"))
    saldo: Mapped[float] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )


    # relationship
    bank: Mapped["Bank"] = relationship("acount")
    user: Mapped["User"] = relationship("acount")