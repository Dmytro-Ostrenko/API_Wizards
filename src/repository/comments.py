from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.database import models 
from src.schemas import schemas_comments

def get_comments(db: Session, photo_id: int) -> List[schemas_comments.Comment]:
    comments = db.query(models.Comment).filter(models.Comment.photo_id == photo_id).all()
    return comments

def create_comment(db: Session, comment: schemas_comments.Comment, photo_id: int, user_id: int):
    db_comment = models.Comment(**comment.dict(), photo_id=photo_id, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(db: Session, comment_id: int, comment: schemas_comments.Comment):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    for var, value in vars(comment).items():
        setattr(db_comment, var, value) if value else None
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(db_comment)
    db.commit()
    return {"ok": True}