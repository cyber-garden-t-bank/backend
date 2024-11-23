"""init6

Revision ID: 98e8ce3330e0
Revises: 08a84f398d83
Create Date: 2024-11-23 14:01:41.451633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98e8ce3330e0'
down_revision: Union[str, None] = '08a84f398d83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bank_user', sa.Column('is_active', sa.Boolean(), nullable=False, server_default=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bank_user', 'is_active')
    # ### end Alembic commands ###
