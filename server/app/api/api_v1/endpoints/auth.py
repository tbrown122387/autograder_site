from datetime import timedelta

from app.api import deps
from app.core import security
from app.core.config import settings
from app.crud import crud_user
from app.models import User
from app.schemas import auth_schema
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

router = APIRouter()


@router.post("/token", response_model=auth_schema.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(deps.get_session)
):
    user = crud_user.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/account")
async def account(current_user: User = Depends(deps.get_current_user)):
    return current_user


@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    session: Session = Depends(deps.get_session)
):
    statement = select(User).where(User.email == email)
    results = session.exec(statement).first()
    if not results:
        password_hash = security.get_password_hash(password)
        new_user = User(email=email, hash_password=password_hash, username=username, name=username[:2])
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code=400, detail="Email already exists")


@router.post("/delete")
def delete_user(
    current_user: User = Depends(deps.get_current_user),
    session: Session = Depends(deps.get_session)
):
    user = session.get(User, current_user.id)
    if user:
        session.delete(user)
        session.commit()
        return user
    else:
        raise HTTPException(status_code=400, detail="This should never happen")


@router.post("/request_password_reset")
def request_password_reset(password_reset: auth_schema.RequestPasswordReset):
    pw_reset_token_expires = timedelta(hours=24)
    pw_reset_token = security.create_access_token(
        data={"sub": password_reset.email}, expires_delta=pw_reset_token_expires
    )
    # send_email(password_reset.email, pw_reset_token)
    return {"pw_reset_token": pw_reset_token}


@router.post("/reset_password_from_token")
def reset_password_from_token(
    pw_reset_body: auth_schema.PasswordResetBody,
    session: Session = Depends(deps.get_session)
):
    token_data = security.decode_jwt(pw_reset_body.pw_reset_token)
    user = crud_user.reset_password(session, token_data.email, pw_reset_body.password)
    if user:
        return user
    else:
        raise HTTPException(status_code=400, detail="There is no account with this email")


@router.post("/reset_password_logged_in")
def reset_password_logged_in(
    current_user: User = Depends(deps.get_current_user),
    password: str = Form(...),
    session: Session = Depends(deps.get_session)
):
    user = crud_user.reset_password(session, current_user.email, password)
    if user:
        return user
    else:
        raise HTTPException(status_code=400, detail="There is no account with this email")


@router.get("/get_users")
def get_users(
    session: Session = Depends(deps.get_session)
):
    statement = select(User)
    results = session.exec(statement)
    return results.all()
