from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class RequestPasswordReset(BaseModel):
    email: str


class EmailSchema(BaseModel):
    email: EmailStr
    name: str
