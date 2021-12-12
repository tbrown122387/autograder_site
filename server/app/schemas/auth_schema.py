from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None


class RequestPasswordReset(BaseModel):
    email: str


class PasswordResetBody(BaseModel):
    pw_reset_token: str
    password: str
