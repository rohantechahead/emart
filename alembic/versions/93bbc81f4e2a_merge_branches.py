"""Merge branches

Revision ID: 93bbc81f4e2a
Revises: 279da212b443, 54c16fb14993
Create Date: 2024-10-09 18:12:17.535236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93bbc81f4e2a'
down_revision: Union[str, None] = ('279da212b443', '54c16fb14993')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
