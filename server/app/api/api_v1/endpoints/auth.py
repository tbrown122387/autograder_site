from datetime import timedelta

from app.api import deps, utils
from app.core import security
from app.core.config import settings
from app.crud import crud_user
from app.models import User, UserToReturn
from app.schemas import auth_schema
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

router = APIRouter()


@router.post("/register", response_model=UserToReturn)
def register(
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    session: Session = Depends(deps.get_session)
):
    results = crud_user.get_user_from_email(session, email)
    if not results:
        password_hash = security.get_password_hash(password)
        new_user = User(email=email, hash_password=password_hash,
                        username=username, name=username[:2])
        user = crud_user.create_user(session, new_user)
        return user
    else:
        raise HTTPException(status_code=400, detail="Email already exists")


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
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/account", response_model=UserToReturn)
async def account(current_user: User = Depends(deps.get_current_user)):
    return current_user


@router.post("/delete", response_model=UserToReturn)
def delete_user(
    current_user: User = Depends(deps.get_current_user),
    session: Session = Depends(deps.get_session)
):
    user = crud_user.delete_user_from_id(session, current_user.id)
    if user:
        return user
    else:  # should never happen
        raise HTTPException(
            status_code=400, detail="There is no account with that email")


@router.post("/request_password_reset")
async def request_password_reset(
        password_reset: auth_schema.RequestPasswordReset,
        session: Session = Depends(deps.get_session),
        fast_mail=Depends(deps.get_fastmail)):
    pw_reset_token_expires = timedelta(minutes=settings.PW_RESET_TOKEN_EXPIRE_MINUTES)
    user = crud_user.get_user_from_email(session, password_reset.email)
    if user:
        pw_reset_token = security.create_access_token(
            data={"sub": password_reset.email},
            expires_delta=pw_reset_token_expires,
            hashed_pw=user.hash_password
        )
        # TODO: don't wait for confirmation?
        await utils.send_pw_reset_email(email=password_reset.email, pw_reset_token=pw_reset_token, fm=fast_mail)
        return {'email': password_reset.email}
    else:
        raise HTTPException(status_code=400, detail="There is no account with this email")


@router.post("/reset_password_from_token", response_model=UserToReturn)
def reset_password_from_token(
    pw_reset_token: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(deps.get_session)
):
    user = crud_user.get_user_from_email(session, email)
    if user:
        token_data = security.decode_jwt(pw_reset_token, hashed_pw=user.hash_password)
        user = crud_user.reset_password(session, token_data.email, password)
        if user:
            return user
        else:
            raise HTTPException(status_code=400, detail="There is no account with this email")
    else:
        raise HTTPException(status_code=400, detail="There is no account with this email")


@router.post("/reset_password_logged_in", response_model=UserToReturn)
def reset_password_logged_in(
    current_user: User = Depends(deps.get_current_user),
    password: str = Form(...),
    session: Session = Depends(deps.get_session)
):
    # Not being used currently
    user = crud_user.reset_password(session, current_user.email, password)
    if user:
        return user
    else:  # should never happen
        raise HTTPException(status_code=400, detail="There is no account with this email")
