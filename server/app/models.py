from typing import Dict, Optional, List
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String, sql
from sqlalchemy.sql import func
import datetime
import sqlalchemy as sa
from sqlmodel.main import Relationship


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: str
    text: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class UserToReturn(SQLModel, table=False):
    id: int = Field(default=None, primary_key=True, nullable=False)
    email: str = Field(sa_column=Column("email", String, unique=True))
    username: str
    name: str


class User(UserToReturn, table=True):
    hash_password: str
    rAssignments: Optional[List["RAssignment"]] = Relationship(back_populates="user")


class RAssignment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    tests_collection: Optional[List[Dict]] = Field(sa_column=Column("tests_collection", sa.JSON, nullable=True))
    bundle_name: Optional[str]
    assignment_name: Optional[str]
    package_names: Optional[str]
    datasets: Optional[List[str]] = Field(sa_column=Column("datasets", sa.JSON, nullable=True))
    setup_code: Optional[str]
    last_modified: datetime.datetime = Field(
        sa_column=sa.Column("last_modified", sa.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()))

    user_id: int = Field(default=None, foreign_key="user.id", nullable=False)
    user: User = Relationship(back_populates="rAssignments")
