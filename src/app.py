from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.models import User
from src.schemas import RootSchema, UserDb, UserPublic, UserPublicList, UserSchema
from src.settings import Settings

app = FastAPI()
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=RootSchema)
def read_root():
    return {'message': 'hello world'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    engine = create_engine(Settings().DATABASE_URL)

    with Session(engine) as session:
        db_user = session.scalar(
            select(User).where((User.username == user.username) | (User.email == user.email))
        )

        if db_user:
            if db_user.username == user.username:
                ...
            elif db_user.email == user.email:
                ...


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserPublicList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDb(**user.model_dump(), id=user_id)

    if user_id < 1 or user_id > len(database):
        raise HTTPException(detail='Not found!', status_code=HTTPStatus.NOT_FOUND)

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(detail='Not found!', status_code=HTTPStatus.NOT_FOUND)

    return database.pop(user_id - 1)
