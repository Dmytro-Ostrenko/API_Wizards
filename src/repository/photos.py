from fastapi import HTTPException
from sqlalchemy import select
from src.schemas.photos import PhotoSchema, PhotoUpdateSchema
from src.database.models import Photos, User, TransformedPhoto
from sqlalchemy.ext.asyncio import AsyncSession
import cloudinary.uploader
from src.database.models import Photos
import qrcode
import os
from src.conf.config import config


UPLOAD_FOLDER = "uploads"




async def upload_photo(file_path: str, user_id: int, db: AsyncSession):
    cloudinary.config(
        cloud_name=config.cloud_name,
        api_key=config.api_key,
        api_secret=config.api_secret
    )
    response = cloudinary.uploader.upload(file_path)
    photo_url = response['url']
    photo = Photos(photo_link=photo_url, user_id=user_id)
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


async def resize_photo(url: str,  width: int, height: int, db: AsyncSession, user: User):
    cloudinary.config(
        cloud_name=config.cloud_name,
        api_key=config.api_key,
        api_secret=config.api_secret
    )
    response = cloudinary.uploader.upload(url, width=width, height=height)
    resized_url = response['url']
    transformed_photo = TransformedPhoto(user_id=user.id, photo_url=resized_url)
    db.add(transformed_photo)
    await db.commit()
    return {"resized_url": resized_url}

async def crop_photo(url: str,  width: int, height: int, db: AsyncSession, user: User):
    cloudinary.config(
        cloud_name=config.cloud_name,
        api_key=config.api_key,
        api_secret=config.api_secret
    )
    response = cloudinary.uploader.upload(url, width=width, height=height, crop="crop")
    cropped_url = response['url']
    transformed_photo = TransformedPhoto(user_id=user.id, photo_url=cropped_url)
    db.add(transformed_photo)
    await db.commit()
    return {"cropped_url": cropped_url}

async def apply_filter_and_text(url: str, filter_name: str, text: str, font_family: str, font_size: int, font_color: str, db: AsyncSession, user: User):
    cloudinary.config(
        cloud_name=config.cloud_name,
        api_key=config.api_key,
        api_secret=config.api_secret
    )
    response = cloudinary.uploader.upload(url, transformation=[
        {"effect": filter_name},
        {"overlay": {"font_family": font_family, "font_size": font_size, "text": text, "font_color": font_color}}
    ])
    edited_url = response['url']
    transformed_photo = TransformedPhoto(user_id=user.id, photo_url=edited_url)
    db.add(transformed_photo)
    await db.commit()
    return {"edited_url": edited_url}

async def convert_photo_format(url: str, new_format: str, db: AsyncSession, user: User):
    cloudinary.config(
        cloud_name=config.cloud_name,
        api_key=config.api_key,
        api_secret=config.api_secret
    )
    response = cloudinary.uploader.upload(url, format=new_format)
    converted_url = response['url']
    transformed_photo = TransformedPhoto(user_id=user.id, photo_url=converted_url)
    db.add(transformed_photo)
    await db.commit()
    return {"converted_url": converted_url}


async def get_photo_metadata(url: str, db: AsyncSession, user: User):
    cloudinary.config(
        cloud_name=config.cloud_name,
        api_key=config.api_key,
        api_secret=config.api_secret
    )
    response = cloudinary.uploader.upload(url)
    metadata = {
        "format": response['format'],
        "width": response['width'],
        "height": response['height'],
        "created_at": response['created_at']
    }
    return metadata


async def generate_transformed_photo_link(transformed_photo_id: int, db: AsyncSession, user: User):
    transformed_photo = await db.get(TransformedPhoto, transformed_photo_id)
    if not transformed_photo:
        raise HTTPException(status_code=404, detail="Transformed photo not found")
    return {"transformed_photo_url": transformed_photo.photo_url}

async def generate_qr_code(transformed_photo_id: int, db: AsyncSession, user: User):
    transformed_image = await db.get(TransformedPhoto, transformed_photo_id)
    if not transformed_image:
        raise HTTPException(status_code=404, detail="Transformed image not found")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(transformed_image.photo_url)
    qr.make(fit=True)

    qr_photo = qr.make_image(fill_color="black", back_color="white")
    os.makedirs("qr_codes", exist_ok=True)
    qr_photo_path = f"qr_codes/transformed_photo_{transformed_photo_id}.png"
    qr_photo.save(qr_photo_path)

    return {"qr_code_url": qr_photo_path}