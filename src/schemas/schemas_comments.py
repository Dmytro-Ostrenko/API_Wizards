from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модель для коментаря
class Comment(BaseModel):
    text: str
    username: Optional[str] = None
    timestamp: Optional[int] = None

# Список для зберігання коментарів
comments: List[Comment] = []

@app.post("/comments/", response_model=Comment)
async def create_comment(comment: Comment):
    comments.append(comment)
    return comment

@app.get("/comments/", response_model=List[Comment])
async def get_comments():
    return comments

@app.put("/comments/{comment_id}", response_model=Comment)
async def update_comment(comment_id: int, comment: Comment):
    if comment_id >= len(comments):
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    comments[comment_id] = comment
    return comment

@app.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int):
    if comment_id >= len(comments):
        raise HTTPException(status_code=404, detail="Коментар не знайдено")
    del comments[comment_id]
    return {"detail": "Коментар видалено"}