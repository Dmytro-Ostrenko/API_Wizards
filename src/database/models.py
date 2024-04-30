import enum
from sqlalchemy import orm, UniqueConstraint
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, DateTime, func, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime, date


class Base(DeclarativeBase):
    pass


class Role(enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"


class Photos(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, unique=True)
    photo_link = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="photos")
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="user_photo")
    tags = relationship("Tags", secondary="photo_tags", back_populates="photos")
    comments = relationship("Comments", back_populates="photo")
    photo_tags = relationship("PhotoTags")
    __table_args__ = (
        UniqueConstraint('photo_link', name='unique_photo_link'),
    )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    role = Column(Enum(Role), default=Role.user, nullable=True)
    confirmed = Column(Boolean, default=False, nullable=True)
    baned = Column(Boolean, default=False, nullable=True)
    photos = relationship("Photos", back_populates="owner")
    user_photo = relationship("Photos", back_populates="user")
    user_comments = relationship("Comments", back_populates="user")



class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, unique=True)
    tag_name = Column(String(150), primary_key=True, unique=True)
    photos = relationship("Photos", secondary="photo_tags", back_populates="tags")
    photo_tags = relationship("PhotoTags", back_populates="tag")



class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    photo_id = Column(Integer, ForeignKey('photos.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    description = Column(String(255), nullable=True)

    photo = relationship("Photos", back_populates="comments")
    user = relationship("User", back_populates="user_comments")

class PhotoTags(Base):
    __tablename__ = "photo_tags"
    photo_id = Column(Integer, ForeignKey('photos.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    photo = relationship("Photos", back_populates="photo_tags")
    tag = relationship("Tags", back_populates="photo_tags")

class TransformedPhoto(Base):
    __tablename__ = "transformed_photos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    photo_url = Column(String, index=True)
    __table_args__ = (
        UniqueConstraint('user_id', 'photo_url', name='unique_user_photo'),
    )