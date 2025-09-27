from pydantic import BaseModel, ConfigDict, EmailStr


class RootSchema(BaseModel):
    message: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublicList(BaseModel):
    users: list[UserPublic]
