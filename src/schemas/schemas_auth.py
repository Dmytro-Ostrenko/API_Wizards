from pydantic import BaseModel, Field
from datetime import datetime

# Модель для користувача
class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
<<<<<<< HEAD
    token_type: str = "bearer"
=======
    token_type: str = "bearer"
>>>>>>> 04b9ae8763d9db3f44897c4241fe9530aaffcdfa
