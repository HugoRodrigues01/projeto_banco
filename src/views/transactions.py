from pydantic import BaseModel

from src.models.transactions import PaymentType, TransactionType


class TransactionView(BaseModel):
    id_transacao: int
    conta_transmissora: int
    conta_destino: int
    valor: int
    tipo_trasacao: TransactionType
    forma_pagamento: PaymentType
