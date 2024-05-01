from fastapi import FastAPI, Query, HTTPException
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

# Initialize SQLAlchemy
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define models
class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    tags = Column(Text)
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


# Define endpoints
@app.get("/photos/")
def search_photos(
    keyword: str = Query(None, min_length=1), 
    tag: str = Query(None, min_length=1), 
    rating: int = Query(None, ge=1, le=5), 
    sort_by: str = Query("date_added", regex="^(date_added|rating)$")
):
    db = SessionLocal()
    photos_query = db.query(Photo)

    # Search by keyword
    if keyword:
        photos_query = photos_query.filter(Photo.title.ilike(f"%{keyword}%") | Photo.description.ilike(f"%{keyword}%"))

    # Search by tag
    if tag:
        photos_query = photos_query.filter(Photo.tags.ilike(f"%{tag}%"))

    # Filter by rating
    if rating:
        photos_query = photos_query.filter(Photo.rating == rating)

    # Sort results
    if sort_by == "date_added":
        photos_query = photos_query.order_by(Photo.created_at.desc())
    elif sort_by == "rating":
        photos_query = photos_query.order_by(Photo.rating.desc())

    photos = photos_query.all()
    return photos

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
