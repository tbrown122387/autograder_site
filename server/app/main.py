from app.models import Comment, User
from fastapi import HTTPException
from pydantic import BaseModel
from app.db import engine
from sqlmodel import Session, select
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.db import create_db_and_tables

app = FastAPI()

origins = [
    "*",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
def health():
    return {"health": "healthy"}


# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()


class DeleteID(BaseModel):
    id: int


@app.post("/comments/create")
def create_comment(comment: Comment):
    comment.id = None

    with Session(engine) as session:
        # make sure user_id exists
        user = session.get(User, comment.user_id)
        if not user:
            comment.user_id = None
        session.add(comment)
        session.commit()
        session.refresh(comment)
    return comment


@app.post("/comments/delete")
def delete_comment(delete_id: DeleteID):
    with Session(engine) as session:
        comment = session.get(Comment, delete_id.id)
        if not comment:
            raise HTTPException(status_code=400, detail="Comment not found")
        session.delete(comment)
        session.commit()
    return comment


@app.get("/comments")
def read_comment():
    with Session(engine) as session:
        heroes = session.exec(select(Comment)).all()
        return heroes
