from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.database.models import User
from src.schemas import schemas_comments 
from src.repository import comments
from src.database.db import get_db
from src.schemas.schemas_comments import CommentUpdateSchema
from src.services.auth import Auth

router = APIRouter(prefix='/comments', tags=["comments"])


@router.get("/comments/{photo_id}/comments", response_model=schemas_comments.Comment)
async def read_comment(photo_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(Auth.get_current_user)):
    db_comment = await comments.get_comments(photo_id, db, user)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.post("/comments/", response_model=schemas_comments.Comment)
async def create_comment_route(comment: schemas_comments.CommentCreate, photo_id: int, user_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(Auth.get_current_user)):
    db_comment = await comments.create_comment(comment=comment, photo_id=photo_id, user_id=user_id, db=db, user=user)
    return db_comment


@router.put("/comments/{comment_id}")
async def update_comment_route(comment_id: int, comment: CommentUpdateSchema, db: AsyncSession = Depends(get_db),
                               user: User = Depends(Auth.get_current_user)):
    if not comment.description:
        raise HTTPException(status_code=400, detail="Description field is required")

    updated_comment = await comments.update_comment(comment_id, comment, db, user)
    if updated_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment

@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(Auth.get_current_user)):
    deleted_comment = delete_comment(comment_id, db, user)
    if not deleted_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}