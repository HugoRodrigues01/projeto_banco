from typing import TYPE_CHECKING, List
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.registry import table_registry

if TYPE_CHECKING:
    from src.models.acounts import Acount

@table_registry.mapped_as_dataclass
class Bank:
    __tablename__ = "table_banco"

    id_bank: Mapped[int] = mapped_column(init=False, primary_key=True)
    bank_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), server_default=func.now()
    )

    acount: Mapped[List["Acount"]] = relationship(back_populates="bank")
