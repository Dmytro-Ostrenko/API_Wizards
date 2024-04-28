import os
import re
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request, status
from src.services.auth import Auth 
from src.database.models import User, Role
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db

from src.routes import auth

import uvicorn

app = FastAPI()



app.include_router(auth.router, prefix="/api")

# Створимо екземпляр класу Auth для використання
auth_service = Auth()


@app.get("/")
async def home_page(request: Request, db: AsyncSession = Depends(get_db)):
    #Створення ролей для юзерів
    roles = ["admin", "moderator", "user"]
    for current_users in roles:
        existing_role = db.query(Role).filter(Role.role == current_users).first()
        if not existing_role:
            db.add(Role(role=current_users))
    db.commit()
    


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    
    

