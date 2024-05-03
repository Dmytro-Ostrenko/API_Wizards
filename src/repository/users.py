from libgravatar import Gravatar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


from src.database.models import User, Role
from src.schemas.schemas_auth import UserModel


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    stmt = select(User).filter(User.email==email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    return user


async def create_user(body: UserModel, db: AsyncSession, role: Role) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the data to be inserted into the database.
            db (Session): The SQLAlchemy Session object used to interact with the database.
        Returns:
            User: A newly created user from the database.

    :param body: UserModel: Create a new user
    :param db: Session: Create a database session
    :return: A user object
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar, role=role.value)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user that will have their token updated
    :param token: str | None: Update the user's refresh token
    :param db: Session: Commit the changes to the database
    :return: None
    """
    user.refresh_token = token
    await db.commit()

async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    The confirmed_email function marks a user as confirmed in the database.
    
    :param email: str: Get the email of the user
    :param db: AsyncSession: Pass in the database session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    The update_avatar_url function updates the avatar url of a user.
    
    :param email: str: Find the user in the database
    :param url: str | None: Specify that the url parameter can be a string or none
    :param db: AsyncSession: Pass in the database session
    :return: A user object
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user

async def get_all_users(db: AsyncSession) -> List[User]:
    """
    The get_all_users function returns a list of all users in the database.
        :return: A list of User objects.
    
    
    :param db: AsyncSession: Pass the database session to the function
    :return: A list of users, but i want to return a json object 
    """
    stmt = select(User)
    user = await db.execute(stmt)
    user = user.scalars().all()
    return user

   

async def update_user_role(email: str, new_role: str, db: AsyncSession) -> User:
    """
    The update_user_role function updates the role of a user in the database.
        Args:
            email (str): The email address of the user to update.
            new_role (str): The new role for this user.
            db (AsyncSession): An async session object from SQLAlchemy's Asyncio engine, which is used to interact with our database.
        Returns:
            User: A User object representing the updated record in our database.
    
    :param email: str: Specify the email of the user to update
    :param new_role: str: Set the new role of the user
    :param db: AsyncSession: Pass the database connection to the function
    :return: The updated user object
    """
    user = await get_user_by_email(email, db)
    user.role = new_role
    await db.commit()
    await db.refresh(user)
    return user