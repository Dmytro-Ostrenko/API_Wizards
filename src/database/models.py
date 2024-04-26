import enum
from sqlalchemy import orm
from sqlalchemy import Column, Integer, String, Date, ForeignKey,  Enum, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from datetime import datetime, date


class Base(orm.DeclarativeBase):
    pass
  
    
class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"
    
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)        
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    role: Mapped[Enum] = mapped_column('role', Enum(Role), default=Role.user, nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    baned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)


    user_photo = relationship("Photo", back_populates="user")
    user_coments = relationship("Сomment", back_populates="user") 
    
    
class Tags(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    #photo_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    tag_name : Mapped[str] = mapped_column(String(150), primary_key=True, unique=True)
    
class Photos(Base):
    __tablename__ = "photos"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    photo_link: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    #tags_id: Mapped[int] = mapped_column(ForeignKey('tags.id'), nullable=True)
    #coments_id: Mapped[int] = mapped_column(ForeignKey('coments.id'), nullable=True)
    description =  mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())


    user = relationship("User", back_populates="user_photo")  
    tags = relationship("Tags", secondary="photo_tags", back_populates="photos")
    comments = relationship("Comments", back_populates="photo")
    
class Coments(Base):
    __tablename__ = "coments"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    photo_id : Mapped[int] = mapped_column(ForeignKey('photos.id')) 
    created_at: Mapped[date] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    description =  mapped_column(String(255), nullable=True)
    
    photo = relationship("Photos", back_populates="comments") 
    user = relationship("User", back_populates="user_coments")

