from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, select

from db import engine
from models import User, Comment
from schemas import DeleteID

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.get("/api/sample")
def sample():
    return {"Hello": "World"}


# def create_heroes():
#     with Session(engine) as session:
#         team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
#         team_z_force = Team(
#             name="Z-Force", headquarters="Sister Margaret’s Bar")
#         session.add(team_preventers)
#         session.add(team_z_force)
#         session.commit()

#         hero_deadpond = Hero(
#             name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
#         )
#         hero_rusty_man = Hero(
#             name="Rusty-Man",
#             secret_name="Tommy Sharp",
#             age=48,
#             team_id=team_preventers.id,
#         )
#         hero_spider_boy = Hero(
#             name="Spider-Boy", secret_name="Pedro Parqueador")
#         session.add(hero_deadpond)
#         session.add(hero_rusty_man)
#         session.add(hero_spider_boy)
#         session.commit()

#         session.refresh(hero_deadpond)
#         session.refresh(hero_rusty_man)
#         session.refresh(hero_spider_boy)

#         print("Created hero:", hero_deadpond)
#         print("Created hero:", hero_rusty_man)
#         print("Created hero:", hero_spider_boy)


# def select_heroes():
#     with Session(engine) as session:
#         statement = select(Hero).where(Hero.age > 20).limit(3)
#         results = session.exec(statement)
#         heroes = results.all()
#         print(heroes)

#         statement = select(Hero, Team).where(Hero.team_id == Team.id)
#         results = session.exec(statement)
#         for hero, team in results:
#             print("Hero:", hero, "Team:", team)


# def update_heroes():
#     with Session(engine) as session:
#         statement = select(Hero).where(Hero.name == "Spider-Boy")
#         results = session.exec(statement)
#         hero = results.one()
#         print("Hero:", hero)

#         hero.age = 16
#         session.add(hero)
#         session.commit()
#         session.refresh(hero)


# def delete_heroes():
#     with Session(engine) as session:
#         statement = select(Hero).where(Hero.name == "Spider-Youngster")
#         results = session.exec(statement)
#         hero = results.one()
#         print("Hero: ", hero)

#         session.delete(hero)
#         session.commit()
#         print("Deleted hero:", hero)

#         statement = select(Hero).where(Hero.name == "Spider-Youngster")
#         results = session.exec(statement)
#         hero = results.first()


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


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def main():
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=5000)


if __name__ == "__main__":
    main()
