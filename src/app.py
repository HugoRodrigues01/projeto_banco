from http import HTTPStatus

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from src.schemas.users import UserSchema
from src.views.users import UserView
from src.models.users import User 
from src.database import get_session

app = FastAPI()


@app.get("/")
def hello():
    return {"Message": "Hello World"}


# USUARIOS
@app.get("/usuarios")
def get_users():
    pass


@app.get("/usuarios/{id}", status_code=HTTPStatus.OK)
def get_user(id: int):
    pass


@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UserView)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.user_email == user.user_email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists."
            )
        elif db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Use email already exists."
            )
    
    db_user = User(
        username=user.username,
        user_email=user.user_email,
        phone_number=user.phone_number,
        password=user.password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put("/usuarios/{id}", status_code=200)
def update_user(id: int):
    pass


@app.delete("/usuarios/{id}")
def delete_user(id: int):
    pass


# CLIENTS
@app.get("/clientes")
def get_clients():
    pass


@app.get("/clientes/{cpf}")
def get_client(cpf: int):
    pass


@app.post("/clientes")
def create_client(client):
    pass


@app.put("/clientes/{cpf}")
def update_client(cpf: int):
    pass


@app.delete("/clientes/{cpf}")
def delete_client(cpf: int):
    pass
