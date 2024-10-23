"""added coloum of country code

Revision ID: f0c355d313bb
Revises: 2873a66c80a6
Create Date: 2024-10-22 16:13:12.873884

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f0c355d313bb'
down_revision: Union[str, None] = '2873a66c80a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('country_code', sa.String(length=10), nullable=True))


def downgrade() -> None:

    ### commands auto generated by Alembic - please adjust! ###
     op.drop_column('users', 'country_code')