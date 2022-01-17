from datetime import datetime, timedelta
from typing import Optional

from app.core.config import settings
from app.schemas.auth_schema import TokenData
from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, hashed_pw: str = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    if hashed_pw:
        encoded_jwt = jwt.encode(to_encode, hashed_pw,
                                 algorithm=settings.ALGORITHM)
    else:
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def decode_jwt_exception(token, hashed_pw: str = None):
    # TODO: combine with decode_jwt
    if token:
        if hashed_pw:
            payload = jwt.decode(token, hashed_pw, algorithms=[
                settings.ALGORITHM])
        else:
            payload = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        return email
    else:
        return None


def decode_jwt(token, hashed_pw: str = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        email = decode_jwt_exception(token, hashed_pw)
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception
