from datetime import UTC, datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    phone_number: int
    user_email: str
    password: str
    created_at: datetime = datetime.now(UTC)
    updated_at: datetime = datetime.now(UTC)


class UserUpdateSchema(BaseModel):
    username: str
    phone_number: int
    user_email: str
    password: str
