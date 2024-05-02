from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


from src.database.models import User, Role


async def get_role_by_name(name: str, db: AsyncSession) -> Role:
    role = Role[name]
    return role