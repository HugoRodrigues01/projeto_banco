from pydantic import BaseModel


class BankSchema(BaseModel):
    bank_name: str
