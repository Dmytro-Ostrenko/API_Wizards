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
    """
    The upload_photo function uploads a photo to the cloudinary server and returns a Photo object.
        Args:
            file_path (str): The path of the image file to be uploaded.
            user_id (int): The id of the user who is uploading this photo.
    
    :param file_path: str: Specify the path of the file to be uploaded
    :param user_id: int: Identify the user who uploaded the photo
    :param db: AsyncSession: Pass the database session to the function
    :return: A photo object
    :doc-author: Trelent
    """
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
    """
    The update_photo function updates a photo in the database.
        Args:
            photo_id (int): The id of the photo to update.
            body (PhotoUpdateSchema): The schema containing the new values for this Photo.
            db (AsyncSession): A database session object, used to query and commit changes to the database.
        Returns:
            Photos: An updated version of this Photo.
    
    :param photo_id: int: Get the photo by id
    :param body: PhotoUpdateSchema: Get the description from the request body
    :param db: AsyncSession: Connect to the database
    :param user: User: Check if the user is an admin or not
    :return: A photo object
    :doc-author: Trelent
    """
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
    """
    The delete_photo function deletes a photo from the database.
        Args:
            photo_id (int): The id of the photo to delete.
            db (AsyncSession): An async session for interacting with the database.
            user (User): The user making this request, used to check permissions.
        Raises:
            HTTPException(403) if the requesting user is not an admin and does not own this resource.
    
    :param photo_id: int: Specify the photo to delete
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Check if the user has permission to delete the photo
    :return: None, which is not a valid response type
    :doc-author: Trelent
    """
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
    """
    The get_photo_by_url function takes a url and returns the photo object associated with that url.
        
    
    :param url: str: Specify the url of the photo
    :param db: AsyncSession: Connect to the database
    :param user: User: Get the user's id
    :return: A photo object
    :doc-author: Trelent
    """
    getting = select(Photos).filter(Photos.photo_link == url)
    photo = await db.execute(getting)
    return photo.scalars().first()


async def resize_photo(url: str, width: int, height: int, db: AsyncSession, user: User):
    """
    The resize_photo function takes a url, width and height as parameters.
    It then uploads the photo to cloudinary with the given dimensions.
    The resized_url is returned in a dictionary.
    
    :param url: str: Pass the url of the photo to be resized
    :param width: int: Set the width of the photo
    :param height: int: Set the height of the photo
    :param db: AsyncSession: Access the database
    :param user: User: Check if the user is authorized to perform this action
    :return: A dictionary with the resized_url key
    :doc-author: Trelent
    """
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
    """
    The crop_photo function crops a photo to the specified width and height.
        Args:
            url (str): The URL of the photo to be cropped.
            width (int): The desired width of the cropped image in pixels.
            height (int): The desired height of the cropped image in pixels.
        Returns: 
            A JSON object containing a single key, &quot;cropped_url&quot;, whose value is 
                a string representing the URL for accessing this newly-cropped image.
    
    :param url: str: Get the url of the photo that needs to be cropped
    :param width: int: Set the width of the cropped photo
    :param height: int: Set the height of the cropped image
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Check if the user has access to the photo
    :return: The cropped_url, but the function is not called in the code
    :doc-author: Trelent
    """
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
    """
    The apply_filter_and_text function applies a filter and text to the photo with the given url.
        Args:
            url (str): The URL of the photo to be edited.
            filter_name (str): The name of the filter to apply.
            text (str): The text that will be added on top of the image.
            font_family (str): Font family for adding text on top of an image, e.g., &quot;Arial&quot;. 
                See https://cloudinary-res.cloudinary.com/image/upload/fl_layer_apply,l_text
    
        Filter Names for Image Processing in Cloudinary and Their Functions:

    - grayscale: Converts the image to grayscale.
    - sepia: Adds a vintage effect to the image.
    - blackwhite: Converts the image to high-contrast black and white.
    - saturation: Controls the color saturation in the image.
    - brightness: Adjusts the brightness of the image.
    - contrast: Controls the contrast between colors in the image.
    - blur: Blurs the image, creating a blur effect.
    - sharpen: Increases the sharpness of the image.
    - hue: Changes the color tone in the image.
    - invert: Inverts the colors in the image.
    :param url: str: Get the url of the photo
    :param filter_name: str: Specify the name of the filter to be applied
    :param text: str: Pass the text that will be written on the photo
    :param font_family: str: Set the font family of the text
    :param font_size: int: Set the font size of the text
    :param font_color: str: Set the color of the text
    :param db: AsyncSession: Create a database session for the function
    :param user: User: Get the user id from the token
    :return: A dictionary with the edited_url key

    """
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
    """
    The convert_photo_format function converts the format of a photo to a new one.
        Args:
            url (str): The URL of the photo to be converted.
            new_format (str): The desired format for the converted photo.
        Returns:
            dict: A dictionary containing information about the transformed image, including its URL and transformation details.
    
    :param url: str: Specify the url of the photo that needs to be converted
    :param new_format: str: Specify the format of the converted photo
    :param db: AsyncSession: Get access to the database
    :param user: User: Get the user id from the token
    :return: A dictionary with the converted_url key
    """
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
    """
    The get_photo_metadata function takes a url and returns the metadata of the photo.
        Args:
            url (str): The URL of the photo to be retrieved.
            db (AsyncSession): An async session for database access.
            user (User): A User object representing who is making this request.
    
    :param url: str: Get the url of the photo
    :param db: AsyncSession: Access the database
    :param user: User: Check the role of the user
    :return: The following:
    """
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
    """
    The generate_transformed_photo_link function is used to generate a link to the transformed photo.
        The function takes in the transformed_photo_id and returns a url for that particular photo.
    
    :param transformed_photo_id: int: Get the transformed photo from the database
    :param db: AsyncSession: Access the database
    :param user: User: Get the user id of the currently logged in user
    :return: A dictionary with the transformed photo url
    """
    transformed_photo = await db.get(TransformedPhoto, transformed_photo_id)
    if not transformed_photo:
        raise HTTPException(status_code=404, detail="Transformed photo not found")
    return {"transformed_photo_url": transformed_photo.photo_url}

async def generate_qr_code(transformed_photo_id: int, db: AsyncSession, user: User):
    """
    The generate_qr_code function generates a QR code for the transformed photo.
        The function takes in the transformed_photo_id and returns a dictionary with
        qr_code url as key and path to the generated QR code as value.
    
    :param transformed_photo_id: int: Get the transformed photo from the database
    :param db: AsyncSession: Access the database
    :param user: User: Check if the user has access to the transformed image
    :return: A dictionary with the key qr_code_url
    """
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
    """
    The create_tag function creates a new tag in the database.
        Args:
            tag_name (str): The name of the new tag to be created.
            db (AsyncSession): An async session object for interacting with the database.
            user (User): A User object representing who is creating this new tag.
        Returns:
            PhotoTags: The newly created PhotoTags object, or None if it already exists.
    
    :param tag_name: str: Pass the tag name to the function
    :param db: AsyncSession: Access the database
    :param user: User: Check if the user has admin rights
    :return: None if the tag does not exist
    """
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
    """
    The attach_tag_to_photo function attaches a tag to a photo.
    
    :param photo_id: int: Specify the photo to which we want to attach a tag
    :param tag_name: str: Specify the name of the tag to be attached
    :param db: AsyncSession: Access the database
    :param user: User: Check if the user is an admin or not
    :return: A tag
    """
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
    """
    The get_tags_for_photo function returns a list of tags for the photo with the given id.
    
    :param photo_id: int: Find the photo in the database
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Check if the user is authorized to view the photo
    :return: A list of tags for a specific photo
    """
    photo = await db.execute(
        select(Photos).filter(Photos.id == photo_id).options(joinedload(Photos.photo_tags))
    )
    photo = photo.scalars().first()
    if (user.role != Role.admin and photo.user_id != user.id):
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo.photo_tags
