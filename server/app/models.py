from typing import Dict, Optional, List
from sqlmodel import Field, SQLModel
from sqlalchemy.sql import func
import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlmodel.main import Relationship


class UserToReturn(SQLModel, table=False):
    id: int = Field(default=None, primary_key=True, nullable=False)
    email: str = Field(sa_column=sa.Column("email", sa.String, unique=True))
    username: str
    name: str


class User(UserToReturn, table=True):
    hash_password: str
    rAssignments: Optional[List["RAssignment"]] = Relationship(back_populates="user", sa_relationship_kwargs={
        "cascade": "all, delete",  # Instruct the ORM how to track changes to local objects
    })


class RAssignment(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, nullable=False)
    tests_collection: Optional[List[Dict]] = Field(sa_column=sa.Column("tests_collection", sa.JSON, nullable=True))
    bundle_name: Optional[str]
    assignment_name: Optional[str]
    package_names: Optional[str]
    datasets: Optional[List[str]] = Field(sa_column=sa.Column("datasets", sa.JSON, nullable=True))
    setup_code: Optional[str]
    last_modified: datetime.datetime = Field(
        sa_column=sa.Column("last_modified", sa.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()))

    # user_id: int = Field(default=None, foreign_key="user.id", nullable=False)
    user_id: int = Field(sa_column=sa.Column("user_id", sa.Integer,
                         sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False))
    # Set the foreign key behavior on the table metadata
    user: User = Relationship(back_populates="rAssignments")
