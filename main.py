import os
import re
from pathlib import Path

from src.services.auth import Auth
from fastapi import FastAPI, Depends, HTTPException, Request, status
import uvicorn
from src.routes import photos
from src.database.models import User, Role
from src.routes import auth
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db

from pydantic import BaseModel
from typing import List


from src.routes import comments

app = FastAPI()


app.include_router(auth.router, prefix="/api")
app.include_router(photos.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
auth_service = Auth()
    



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
