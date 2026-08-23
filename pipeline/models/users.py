from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    user_id: int
    email: str
    password_hash: str
    created_at: datetime

class UserCreate(BaseModel):
    email: str
    password: str

class UserGet(BaseModel):
    user_id: int | None = None
    email: str | None = None
    created_at: datetime | None = None

class UserUpdate(BaseModel):
    email: str | None = None
    password: str | None = None

class UserDelete(BaseModel):
    user_id: int

    

    