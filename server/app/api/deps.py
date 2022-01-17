from typing import Generator

from app.core.config import conf, settings
from app.core.security import decode_jwt
from app.crud.crud_user import get_user_from_email
from app.db import engine
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import FastMail
from sqlmodel import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token", auto_error=False)
fm = FastMail(conf)


def get_fastmail():
    return fm


def get_session() -> Generator:
    with Session(engine) as session:
        yield session


class CurrentUser:
    def __init__(self, optional: bool):
        self.optional = optional

    async def __call__(self, token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
        try:
            token_data = decode_jwt(token)
        except HTTPException as error:
            if self.optional:
                return None
            else:
                raise error

        user = get_user_from_email(session, token_data.email)

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if self.optional or user:
            return user
        else:
            raise credentials_exception


get_current_user = CurrentUser(optional=False)
optional_get_current_user = CurrentUser(optional=True)
