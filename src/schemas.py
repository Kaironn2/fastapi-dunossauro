from pydantic import BaseModel, EmailStr


class RootSchema(BaseModel):
    message: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str


class UserPublicList(BaseModel):
    users: list[UserPublic]
