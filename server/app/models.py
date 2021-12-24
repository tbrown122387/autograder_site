from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    text: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column("email", String, unique=True))
    hash_password: str
    username: str
    name: str
