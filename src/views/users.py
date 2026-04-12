from pydantic import BaseModel


class UserView(BaseModel):
    user_id: int
    user_name: str
    email: str
