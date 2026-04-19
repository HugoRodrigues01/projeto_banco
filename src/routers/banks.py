import logging
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.deps import T_Session
from src.models.banks import Bank
from src.schemas.banks import BankSchema
from src.views.banks import BankListView, BankView

router = APIRouter(prefix="/bancos", tags=["bancos"])

logging.basicConfig(level=logging.DEBUG)


@router.get("/{id}", status_code=HTTPStatus.OK, response_model=BankView)
def get_bank(id: int, session: T_Session):
    bank = session.scalar(select(Bank).where(Bank.id_bank == id))

    if not bank:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Bank with id {id} not found.",
        )

    return bank


@router.get("/", status_code=HTTPStatus.OK, response_model=BankListView)
def get_banks(session: T_Session, skip: int = 0, limit: int = 10):
    banks = session.scalars(select(Bank).offset(skip).limit(limit)).all()

    return {"banks": banks}


@router.post("/", status_code=HTTPStatus.CREATED, response_model=BankView)
def create_bank(bank: BankSchema, session: T_Session):
    new_bank = session.scalar(
        select(Bank).where(Bank.bank_name == bank.bank_name)
    )

    if new_bank:
        if new_bank.bank_name == bank.bank_name:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Bank name already exists.",
            )

    new_bank = Bank(bank_name=bank.bank_name)
    session.add(new_bank)
    session.commit()
    session.refresh(new_bank)

    return new_bank
