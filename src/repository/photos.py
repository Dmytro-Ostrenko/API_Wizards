from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, func

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


from src.schemas.photos import PhotoSchema, PhotoUpdateSchema
from src.database.models import Photos, User, TransformedPhoto, PhotoTags, TagAssociation, Role
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
    getting = select(Photos).filter(Photos.id == photo_id)
    result = await db.execute(getting)
    photo = result.scalar_one_or_none()
    if (user.role != Role.admin and photo.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    if photo:
        photo.description = body.description
        await db.commit()
        await db.refresh(photo)
    return photo


async def delete_photo(photo_id: int, db: AsyncSession, user: User) -> None:
    getting = select(Photos).filter(Photos.id == photo_id)
    result = await db.execute(getting)
    photo = result.scalar_one_or_none()
    if (user.role != Role.admin and photo.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    if photo:
        await db.delete(photo)
        await db.commit()
    return photo

async def get_photo_by_url(url: str, db: AsyncSession, user: User):
    getting = select(Photos).filter(Photos.photo_link == url)
    photo = await db.execute(getting)
    return photo.scalars().first()


async def resize_photo(url: str, width: int, height: int, db: AsyncSession, user: User):
    cloudinary.config(
        cloud_name=config.cloud_name,
        api_key=config.api_key,
        api_secret=config.api_secret
    )
    response = cloudinary.uploader.upload(url, width=width, height=height)
    resized_url = response['url']
    photo = await get_photo_by_url(url, db, user)
    if (user.role != Role.admin and photo.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
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
    photo = await get_photo_by_url(url, db, user)
    if (user.role != Role.admin and photo.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
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
    photo = await get_photo_by_url(url, db, user)
    if (user.role != Role.admin and photo.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
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
    photo = await get_photo_by_url(url, db, user)
    if (user.role != Role.admin and photo.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
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
    photo = await get_photo_by_url(url, db, user)
    if (user.role != Role.admin and photo.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
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
    if (user.role != Role.admin and transformed_image.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
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


async def create_tag(tag_name: str, db: AsyncSession, user: User):
    existing_tag = await db.execute(select(PhotoTags).filter_by(tag_name=tag_name))
    existing_tag = existing_tag.scalar_one_or_none()
    if (user.role != Role.admin and existing_tag.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    if not existing_tag:
        tag = PhotoTags(tag_name=tag_name)
        db.add(tag)
        await db.flush()
        await db.commit()
    return existing_tag


async def attach_tag_to_photo(photo_id: int, tag_name: str, db: AsyncSession, user: User):
    photo = await db.get(Photos, photo_id)
    if (user.role != Role.admin and photo.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    # Проверяем, существует ли тег с заданным именем
    tag_query = select(PhotoTags).where(PhotoTags.tag_name == tag_name)
    tag_result = await db.execute(tag_query)
    tag = tag_result.scalar_one_or_none()
    if tag is None:
        raise HTTPException(status_code=404, detail=f"Tag '{tag_name}' not found")

    # Проверяем количество тегов, используя запрос к базе данных
    count_tags_query = select(func.count()).where(TagAssociation.photo_id == photo_id)
    count_tags_result = await db.execute(count_tags_query)
    count_tags = count_tags_result.scalar_one()

    if count_tags >= 5:
        raise HTTPException(status_code=400, detail="Maximum number of tags reached for this photo")
    tag_association = TagAssociation(photo_id=photo_id, tag_id=tag.tag_id)

    db.add(tag_association)
    await db.commit()

    return tag




from sqlalchemy.orm import joinedload

async def get_tags_for_photo(photo_id: int, db: AsyncSession, user: User):
    photo = await db.execute(
        select(Photos).filter(Photos.id == photo_id).options(joinedload(Photos.photo_tags))
    )
    photo = photo.scalars().first()
    if (user.role != Role.admin and photo.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo.photo_tags

