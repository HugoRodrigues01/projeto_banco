from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models.users import User
from src.schemas.users import UserSchema, UserUpdateSchema
from src.views.users import UserListView, UserView

app = FastAPI()


@app.get("/")
def hello():
    return {"Message": "Hello World"}


# USUARIOS
@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=UserListView)
def get_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users}


@app.get("/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UserView)
def get_user(id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.user_id == id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User id not exists."
        )

    return user


@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UserView)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username)
            | (User.user_email == user.user_email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists.",
            )
        elif db_user.user_email == user.user_email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Use email already exists.",
            )

    db_user = User(
        username=user.username,
        user_email=user.user_email,
        phone_number=user.phone_number,
        password=user.password,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put(
    "/usuarios/{id}", status_code=HTTPStatus.CREATED, response_model=UserView
)
def update_user(
    id: int,
    new_user: UserUpdateSchema,
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.user_id == id))

    if user:
        update_user = user
        update_user.username = new_user.username
        update_user.user_email = new_user.user_email or user.user_email
        update_user.password = new_user.password or user.password
        update_user.phone_number = new_user.phone_number or user.phone_number

        session.add(update_user)
        session.commit()
        session.refresh(update_user)

    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User do not exists."
        )

    return update_user


@app.delete(
    "/usuarios/{id}", status_code=HTTPStatus.OK, response_model=UserView
)
def delete_user(id: int, session: Session = Depends(get_session)):

    user = session.scalar(select(User).where(User.user_id == id))

    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User do not exists."
        )

    return user


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
