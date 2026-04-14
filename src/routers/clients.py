from fastapi import APIRouter

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/clientes")
def get_clients():
    pass


@router.get("/clientes/{cpf}")
def get_client(cpf: int):
    pass


@router.post("/clientes")
def create_client(client):
    pass


@router.put("/clientes/{cpf}")
def update_client(cpf: int):
    pass


@router.delete("/clientes/{cpf}")
def delete_client(cpf: int):
    pass
