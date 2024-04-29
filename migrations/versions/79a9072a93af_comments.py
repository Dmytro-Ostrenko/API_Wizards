"""comments

Revision ID: 79a9072a93af
Revises: 598cf5a35a51
Create Date: 2024-04-29 06:59:57.817085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79a9072a93af'
down_revision: Union[str, None] = '598cf5a35a51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
