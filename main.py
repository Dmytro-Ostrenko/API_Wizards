

from src.services.auth import Auth
from fastapi import FastAPI, Depends, HTTPException, Request, status
import uvicorn
from src.routes import photos
from src.database.models import User, Role
from src.routes import auth
from src.database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

app.include_router(photos.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
auth_service = Auth()


@app.get("/")
async def home_page(request: Request, db: AsyncSession = Depends(get_db)):
    # Створення ролей для юзерів
    roles = ["admin", "moderator", "user"]
    for current_users in roles:
        existing_role = db.query(Role).filter(Role.role == current_users).first()
        if not existing_role:
            db.add(Role(role=current_users))
    db.commit()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    
    

