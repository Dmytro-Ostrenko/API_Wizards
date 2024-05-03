from typing import List
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from src.database.models import Comments, User
from src.schemas import schemas_comments
from sqlalchemy import select, func

async def get_comments(photo_id: int, db: AsyncSession, user: User):
    """
    The get_comments function takes in a photo_id and returns all comments associated with that photo.
        
    
    :param photo_id: int: Get the comments for a specific photo
    :param db: AsyncSession: Pass the database connection to the function
    :param user: User: Get the user's id, which is used to check if they have liked a comment or not
    :return: A list of comments, so the following function should be used instead:

    """
    getting = select(Comments).filter(Comments.photo_id == photo_id)
    comments = await db.execute(getting)
    return comments.scalars().one_or_none()

async def create_comment(comment: schemas_comments.CommentCreate, photo_id: int, user_id: int, db: AsyncSession, user: User):
    """
    The create_comment function creates a comment for a photo.
        Args:
            comment (schemas_comments.CommentCreate): The CommentCreate schema object that contains the description of the new comment to be created.
            photo_id (int): The id of the photo that is being commented on.
            user_id (int): The id of the user who is creating this new comment.&lt;/code&gt;
    
    :param comment: schemas_comments.CommentCreate: Create a new comment
    :param photo_id: int: Get the photo id from the url
    :param user_id: int: Get the user_id of the user who created the comment
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Check if the user is authenticated
    :return: The db_comment object

    """
    db_comment = Comments(
        user_id=user_id,
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
        Args:
            comment_id (int): The id of the comment to be updated.
            comment (schemas_comments.CommentUpdateSchema): The new description for the specified Comment object.
            db (AsyncSession): An async session with an open connection to a PostgreSQL database server, as defined in main().
            user (User): A User object containing information about who is making this request, as defined by FastAPI's @get_current_user() decorator and passed into this function by its parent function update().
    
    :param comment_id: int: Identify the comment that is being updated
    :param comment: schemas_comments.CommentUpdateSchema: Get the comment from the request body
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Check if the user is the owner of the comment
    :return: A comment object, which is a sqlalchemy model

    """
    getting = select(Comments).filter(Comments.id == comment_id)
    result = await db.execute(getting)
    db_comment = result.scalar_one_or_none()
    if db_comment:
        db_comment.description = comment.description
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def delete_comment(comment_id: int, db: AsyncSession, user: User):
    """
    The delete_comment function deletes a comment from the database.
        Args:
            comment_id (int): The id of the comment to be deleted.
            db (AsyncSession): An async session object for interacting with the database.
            user (User): A User object representing who is making this request.
    
    :param comment_id: int: Find the comment in the database
    :param db: AsyncSession: Pass in the database session
    :param user: User: Pass the user object to the function
    :return: A comment object

    """
    getting = select(Comments).filter(Comments.id == comment_id)
    result = await db.execute(getting)
    db_comment = result.scalar_one_or_none()
    if db_comment:
        if db_comment.user_id != user.id:
            raise HTTPException(status_code=403, detail="You do not have permission to delete this comment")
        await db.delete(db_comment)
        await db.flush()
        await db.commit()
    return db_comment