from sqlalchemy import select
from src.schemas.photos import PhotoSchema, PhotoUpdateSchema
from src.database.models import Photos, User
from sqlalchemy.ext.asyncio import AsyncSession
import cloudinary.uploader
from src.database.models import Photos


async def upload_photo(file_path: str, user_id: int, db: AsyncSession):
    cloudinary.config(
        cloud_name="dsm1gklce",
        api_key="873821538232998",
        api_secret="ebVxlgXmxbDmNI-GZBS3iAg0Hzg"
    )
    response = cloudinary.uploader.upload(file_path)
    photo_url = response['url']
    photo = Photos(photo_link=photo_url, user_id=user_id)

    # Зберігання фото в базі даних
    db.add(photo)
    await db.commit()

    return photo
async def update_photo(photo_id: int,body: PhotoUpdateSchema, db: AsyncSession, user: User) -> Photos:
    getting = select(Photos).filter_by(id=photo_id, user=user)
    result = await db.execute(getting)
    photo = result.scalar_one_or_none()
    if photo:
        photo.description = body.description
        await db.commit()
        await db.refresh(photo)
    return photo


async def delete_photo(photo_id: int, db: AsyncSession, user: User) -> None:
    getting = select(Photos).filter_by(id=photo_id, user=user)
    result = await db.execute(getting)
    photo = result.scalar_one_or_none()
    if photo:
        await db.delete(photo)
        await db.commit()
    return photo

async def get_photo_by_url(url: str, db: AsyncSession, user: User):
    getting = select(Photos).filter(Photos.photo_link == url)
    photo = await db.execute(getting)
    return photo.scalars().first()