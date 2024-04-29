from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.database.models import User, Role
from src.repository import photos
from src.schemas.photos import PhotoUpdateSchema
from src.services.auth import Auth
from src.services.roles import RoleAccess

router = APIRouter(prefix='/photos', tags=['photos'])

access_to_route_all = RoleAccess([Role.admin, Role.moderator])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_photo_route(file: UploadFile = File(...), db: AsyncSession = Depends(get_db),
                             user: User = Depends(Auth.get_current_user)):
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(await file.read())
        file_path = temp_file.name
        photo = await photos.upload_photo(file_path=file_path, user_id=user.id, db=db)

    return {"message": "Зображення було успішно завантажено"}


@router.put("/photos/{photo_id}")
async def update_photo(body: PhotoUpdateSchema, photo_id: int, description: str, db: AsyncSession = Depends(get_db),
                       user: User = Depends(Auth.get_current_user)):
    photo = await photos.update_photo(photo_id, body, db, user)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return {"message": f"Опис зображення з ідентифікатором {photo_id} було успішно оновлено"}

@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(photo_id: int, db: AsyncSession = Depends(get_db),
                       user: User = Depends(Auth.get_current_user)):
    photo = await photos.delete_photo(photo_id, db, user)
    return {"message": f"Зображення з ідентифікатором {photo_id} було успішно видалено"}

from datetime import datetime
from fastapi import HTTPException

@router.get("/photos/")
async def get_image(url: str = Query(...), db: AsyncSession = Depends(get_db),
                    user: User = Depends(Auth.get_current_user)):
    photo = await photos.get_photo_by_url(url, db, user)
    if photo:
        return {"title": f"Зображення з унікальним посиланням",
                "description": photo.description,
                "completed": False,
                "created_at": photo.created_at,
                "updated_at": photo.updated_at}
    else:
        raise HTTPException(status_code=404, detail="Зображення не знайдено")