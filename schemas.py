from datetime import datetime

from pydantic import BaseModel

# USER
class CreateUser(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

class Token(BaseModel):
    access_token: str


# NOTE
class UserNote(BaseModel):
    name: str
    content: str

class DbNote(UserNote):
    id: int
    username: str
    created_at: datetime