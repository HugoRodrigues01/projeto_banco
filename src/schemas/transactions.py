from pydantic import BaseModel

from src.models.transactions import PaymentType, TransactionType


class TransactionSchema(BaseModel):
    conta_destino: int
    valor: float
    tipo_transacao: TransactionType
    forma_pagamento: PaymentType
