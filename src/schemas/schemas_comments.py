from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модель для коментаря
class Comment(BaseModel):
    id: int
    user_id: int
    photo_id: int
    created_at: datetime
    updated_at: datetime
    description: str

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    description: str
    user_id: int
    photo_id: int

class CommentUpdateSchema(BaseModel):
    description: str