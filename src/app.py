from http import HTTPStatus
from typing import cast

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.exceptions import AppError
from src.models import User
from src.schemas import RootSchema, Token, UserPublic, UserPublicList, UserSchema
from src.security import create_access_token, get_password_hash, verify_password

app = FastAPI()
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=RootSchema)
def read_root():
    return {'message': 'hello world'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:
        if db_user.username == user.username:
            AppError.http_exception('BAD_REQUEST', 'Username already exists.')
        elif db_user.email == user.email:
            AppError.http_exception('BAD_REQUEST', 'Email already exists.')

    db_user = User(
        username=user.username, email=user.email, password=get_password_hash(user.password)
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserPublicList)
def read_users(limit: int = 10, offset: int = 0, session: Session = Depends(get_session)):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = cast(User, session.scalar(select(User).where(User.id == user_id)))

    if not db_user:
        AppError.http_exception('NOT_FOUND', 'This user does not exists')

    return db_user


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    db_user = cast(User, session.scalar(select(User).where(User.id == user_id)))

    if not db_user:
        AppError.http_exception('NOT_FOUND', 'This user does not exists')

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', status_code=HTTPStatus.OK)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        AppError.http_exception('NOT_FOUND', 'This user does not exists')

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}


@app.post('/token/', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException()

    access_token = create_access_token(data={'sub': user.email})
