from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Comments, User
from src.schemas import schemas_comments
from sqlalchemy import select, func


async def get_comments(photo_id: int, db: AsyncSession, user: User):
    getting = select(Comments).filter(Comments.photo_id == photo_id)

    comments = await db.execute(getting)
    return comments.scalars().one_or_none()


async def create_comment(comment: schemas_comments.CommentCreate, photo_id: int, user_id: int, db: AsyncSession, user: User):
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
    getting = select(Comments).filter(Comments.id == comment_id)
    result = await db.execute(getting)
    db_comment = result.scalar_one_or_none()
    if db_comment:
        db_comment.description = comment.description
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def delete_comment(comment_id: int, db: AsyncSession, user: User):
    getting = select(Comments).filter(Comments.id == comment_id)
    result = await db.execute(getting)
    db_comment = result.scalar_one_or_none()
    if db_comment:
        await db.delete(db_comment)
        await db.commit()
    return db_comment