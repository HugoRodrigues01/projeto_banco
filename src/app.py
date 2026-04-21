from fastapi import FastAPI

from src.routers import accounts, banks, token, transactions, users

app = FastAPI()
app.include_router(users.router)
app.include_router(token.router)
app.include_router(banks.router)
app.include_router(accounts.router)
app.include_router(transactions.router)


@app.get("/")
def hello():
    return {"Message": "Hello World"}
