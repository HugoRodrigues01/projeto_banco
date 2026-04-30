from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.models.transactions import PaymentType, TransactionType


class TransactionView(BaseModel):
    id_transacao: int
    conta_transmissora: int
    conta_destino: int
    valor: float
    tipo_trasacao: TransactionType
    forma_pagamento: PaymentType
    created_at: datetime


class TransactionListView(BaseModel):
    extract: List[TransactionView]

    class Config:
        orm_mode = True
