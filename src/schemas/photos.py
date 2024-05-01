from typing import List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.schemas.user import UserResponse

class PhotoSchema(BaseModel):
    url: str
    description: str = Field(min_length=3, max_length=250)
    tags: List[str] = Field(max_length=5)

class PhotoUpdateSchema(PhotoSchema):
    completed: bool

class PhotoResponse(BaseModel):
    id: int = 1
    title: str
    description: str
    completed: bool
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None

    model_config = ConfigDict(from_attributes = True)

class TransformedImageCreate(BaseModel):
    user_id: int
    image_url: str
    transformation: str