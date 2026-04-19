from fastapi import FastAPI

from src.routers import banks, token, users

app = FastAPI()
app.include_router(users.router)
app.include_router(token.router)
app.include_router(banks.router)


@app.get("/")
def hello():
    return {"Message": "Hello World"}
