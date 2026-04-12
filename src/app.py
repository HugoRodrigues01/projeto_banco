from http import HTTPStatus

from fastapi import FastAPI

from src.schemas.users import UserSchema
from src.views.users import UserView

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
def create_user(user: UserSchema):
    pass


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
