from pydantic import BaseModel


class BankView(BaseModel):
    id_bank: int
    bank_name: str


class BankListView(BaseModel):
    banks: list[BankView]
