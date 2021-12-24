from typing import Optional

from fastapi.exceptions import HTTPException

from app.core.security import get_password_hash, verify_password
from app.models import Comment, User
from sqlmodel import Session, select


def reset_password(session: Session, email: str, password: str):
    statement = select(User).where(User.email == email)
    user: Optional[User] = session.exec(statement).first()
    if user:
        user.hash_password = get_password_hash(password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    else:
        return None


def authenticate_user(session: Session, username: str, password: str):
    user = get_user_from_email(session=session, email=username)
    if not user:
        return False
    if not verify_password(password, user.hash_password):
        return False
    return user


def get_user_from_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    results = session.exec(statement).first()
    if results:
        return results


def delete_user_from_id(session: Session, id: int):
    user = session.get(User, id)
    if user:
        session.delete(user)
        session.commit()
        return user


def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
