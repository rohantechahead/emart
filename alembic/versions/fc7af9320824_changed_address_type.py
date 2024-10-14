"""changed address type

Revision ID: fc7af9320824
Revises: 7cdfb12cdfc2
Create Date: 2024-10-14 15:58:25.554673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'fc7af9320824'
down_revision: Union[str, None] = '7cdfb12cdfc2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('useraddresses', sa.Column('address_type', sa.String(length=50), nullable=False))
    op.drop_column('useraddresses', 'type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('useraddresses', sa.Column('type', mysql.VARCHAR(length=50), nullable=False))
    op.drop_column('useraddresses', 'address_type')
    # ### end Alembic commands ###
