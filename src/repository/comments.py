from typing import List
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.database.models import Comments, User, Role
from src.services.auth import Auth
from src.schemas import schemas_comments
from sqlalchemy import select, func
from fastapi import APIRouter, Depends, HTTPException
from src.database.db import get_db
from src.repository import roles
async def get_comments(photo_id: int, db: AsyncSession, user: User):
    """
    The get_comments function takes in a photo_id and returns all comments associated with that photo.
        
    
    :param photo_id: int: Get the comments for a specific photo
    :param db: AsyncSession: Connect to the database
    :param user: User: Get the user_id of the user who is logged in
    :return: A list of comments
    """
    getting = select(Comments).filter(Comments.photo_id == photo_id)
    comments = await db.execute(getting)
    return comments.scalars().one_or_none()
async def create_comment(comment: schemas_comments.CommentCreate, photo_id: int, db: AsyncSession, user: User):
    """
    The create_comment function creates a new comment in the database.
        Args:
            comment (schemas_comments.CommentCreate): The CommentCreate schema object that contains the data for creating a new comment.
            photo_id (int): The id of the photo to which this comment belongs to.
            db (AsyncSession): An async SQLAlchemy session object used for querying and modifying data in our database tables/models/entities, etc...
            user (User): A User model instance representing an authenticated user who is making this request to create a new comment on their own behalf. This
    
    :param comment: schemas_comments.CommentCreate: Pass the data from the request body to create_comment function
    :param photo_id: int: Get the photo_id from the url
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user_id from the user object
    :return: An object of type comments
    """
    db_comment = Comments(
        user_id=user.id,  # Отримуємо user_id з об'єкта користувача
        photo_id=photo_id,
        created_at=func.now(),
        updated_at=func.now(),
        description=comment.description
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment
async def update_comment(comment_id: int, comment: schemas_comments.CommentUpdateSchema, db: AsyncSession, user: User):
    """
    The update_comment function updates a comment in the database.
        It takes an integer comment_id, a CommentUpdateSchema object called comment, and an AsyncSession object called db.
        The function first gets the existing comment from the database using its id number.
        If it exists, then it checks to see if the user who is trying to update this post is actually its author by comparing their ids.
        If they are not equal (i.e., if they are not one and the same), then we raise a 403 error because that user does not have permission to update this post.
    
    :param comment_id: int: Find the comment to update
    :param comment: schemas_comments.CommentUpdateSchema: Get the description from the request body
    :param db: AsyncSession: Connect to the database
    :param user: User: Check if the user has permission to update the comment
    :return: A comment object
    """
    getting = select(Comments).filter(Comments.id == comment_id)
    result = await db.execute(getting)
    db_comment = result.scalar_one_or_none()
    if db_comment:
        if db_comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to update this comment")
        db_comment.description = comment.description
        await db.commit()
        await db.refresh(db_comment)
        return db_comment
    else:
        raise HTTPException(status_code=404, detail="Comment not found")
async def delete_comment(comment_id: int, db: AsyncSession, user: User) -> None:
    """
    The delete_comment function deletes a comment from the database.
        Args:
            comment_id (int): The id of the comment to delete.
            db (AsyncSession): An async session for interacting with the database.
            user (User): The user making this request, used to check permissions.
        Raises:
            HTTPException(403) if the requesting user is not an admin or moderator.
    :param comment_id: int: Specify the comment to delete
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Check if the user has permission to delete the comment
    """
    getting = select(Comments).filter(Comments.id == comment_id)
    result = await db.execute(getting)
    comment = result.scalar_one_or_none()
    if user.role != Role.admin and user.role != Role.moderator:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    if comment:
        await db.delete(comment)
        await db.commit()
    return comment
