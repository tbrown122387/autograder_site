from typing import Generator

from app.core.config import settings
from app.core.security import decode_jwt
from app.crud.crud_user import get_user_from_email
from app.db import engine
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")


def get_session() -> Generator:
    with Session(engine) as session:
        yield session


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    token_data = decode_jwt(token)
    user = get_user_from_email(session, token_data.email)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if user is None:
        raise credentials_exception
    return user
