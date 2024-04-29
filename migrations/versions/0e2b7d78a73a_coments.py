"""coments

Revision ID: 0e2b7d78a73a
Revises: d35ee28fdd70
Create Date: 2024-04-29 07:04:24.448355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e2b7d78a73a'
down_revision: Union[str, None] = 'd35ee28fdd70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
