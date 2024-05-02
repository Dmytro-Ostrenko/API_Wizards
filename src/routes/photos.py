from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, status, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.database.models import User, Role
from src.repository import photos
from src.schemas.photos import PhotoUpdateSchema, PhotoTagsSchema, GetTagsSchema
from src.services.auth import Auth
from src.services.roles import RoleAccess

from fastapi import HTTPException
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



@router.post("/photos/resize", status_code=status.HTTP_200_OK)
async def resize_photo(url: str, width: int, height: int, db: AsyncSession = Depends(get_db),
                       user: User = Depends(Auth.get_current_user)):
    result = await photos.resize_photo(url, width, height, db, user)
    resized_photo = result['resized_url']

    return {"resized_photo": resized_photo}



@router.post("/photos/crop", status_code=status.HTTP_200_OK)
async def crop_photo(url: str, width: int, height: int, db: AsyncSession = Depends(get_db),
                     user: User = Depends(Auth.get_current_user)):
    result = await photos.crop_photo(url, width, height, db, user)
    cropped_photo = result['cropped_url']
    return {"cropped_photo": cropped_photo}

@router.post("/photos/apply-filter-text", status_code=status.HTTP_200_OK)
async def apply_filter_text_route(url: str, filter_name: str, text: str, font_family: str, font_size: int, font_color: str,
                                  db: AsyncSession = Depends(get_db), user: User = Depends(Auth.get_current_user)):
    result = await photos.apply_filter_and_text(url, filter_name, text, font_family, font_size, font_color, db, user)
    edited_url = result['edited_url']
    return {"edited_url": edited_url}

@router.post("/photos/convert-format", status_code=status.HTTP_200_OK)
async def convert_photo_format_route(url: str, new_format: str, db: AsyncSession = Depends(get_db),
                                     user: User = Depends(Auth.get_current_user)):
    result = await photos.convert_photo_format(url, new_format, db, user)
    converted_url = result['converted_url']
    return {"converted_url": converted_url}

@router.post("/photos/get-metadata", status_code=status.HTTP_200_OK)
async def get_photo_metadata_route(url: str, db: AsyncSession = Depends(get_db),
                                   user: User = Depends(Auth.get_current_user)):
    metadata = await photos.get_photo_metadata(url, db, user)
    return metadata

@router.get("/photos/{transformed_photo_id}", response_model=dict)
async def get_transformed_photo_link(transformed_photo_id: int, db: AsyncSession = Depends(get_db),
                                      user: User = Depends(Auth.get_current_user)):
    transformed_link = await photos.generate_transformed_photo_link(transformed_photo_id, db, user)
    return {"transformed_link": transformed_link}

@router.get("/photos/get_qr_code/{transformed_photo_id}/", response_model=dict)
async def get_qr_code(transformed_photo_id: int, db: AsyncSession = Depends(get_db),
                      user: User = Depends(Auth.get_current_user)):
    qr_code = await photos.generate_qr_code(transformed_photo_id, db, user)
    return qr_code

@router.post("/photos/tags/", response_model=PhotoTagsSchema)
async def create_photo_tag(tag_name: str, db: AsyncSession = Depends(get_db), user: User = Depends(Auth.get_current_user)):
    tag = await photos.create_tag(tag_name, db, user)
    return PhotoTagsSchema(tag_name=tag.tag_name)

@router.post("/photos/{photo_id}/tags/{tag_id}/attach")
async def attach_tag_to_photo_route(photo_id: int, tag_name: str, db: AsyncSession = Depends(get_db), user: User = Depends(Auth.get_current_user)):
    photo_tag = await photos.attach_tag_to_photo(photo_id, tag_name, db, user)
    return {"message": f"Теги {photo_tag} були додани до зображення з ID {photo_id}"}

@router.get("/photos/get_tag/{photo_id}/tags", response_model=GetTagsSchema)
async def get_photo_tags(photo_id: int, db: AsyncSession = Depends(get_db),
                         user: User = Depends(Auth.get_current_user)):
    tags = await photos.get_tags_for_photo(photo_id, db, user)
    return {"tags": tags}