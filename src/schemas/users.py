from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    number: int
    user_email: str
    password: str
    created_at: datetime
    updated_at: datetime
