from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class User(SQLModel, table = True):
    id : int | None = Field(default= None, primary_key = True)
    username : str
    hashed_password: str

class Note(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key = True)
    name: str
    content: str
    username: str
    created_at: datetime | None = Field(default_factory=lambda:datetime.now(timezone.utc))