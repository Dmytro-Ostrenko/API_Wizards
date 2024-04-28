import os
import re
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request, status
from src.services.auth import Auth # Імпорт класу Auth та класу UserRole з auth.py
from src.database.models import User, Role
import uvicorn

app = FastAPI()



# Створимо екземпляр класу Auth для використання
auth_service = Auth()

@app.get("/")
def index():
    return {'message': 'PhotoShare Application'}

# Додамо приклад використання класу Auth
@app.get("/protected-route")
async def protected_route(current_user: User = Depends(auth_service.get_current_user(role=Role.ADMIN))):
    return {"message": "Welcome to the protected route, Admin!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    
    

