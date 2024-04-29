"""coments

Revision ID: b8ddc9fe7d52
Revises: 79a9072a93af
Create Date: 2024-04-29 07:02:23.445058

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8ddc9fe7d52'
down_revision: Union[str, None] = '79a9072a93af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
