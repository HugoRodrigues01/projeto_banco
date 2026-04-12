from pydantic import BaseModel


class UserView(BaseModel):
    user_id: int
    username: str
    user_email: str


class UserListView(BaseModel):
    users: list[UserView]
