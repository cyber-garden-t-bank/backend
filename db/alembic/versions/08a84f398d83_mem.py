"""mem

Revision ID: 08a84f398d83
Revises: 00fda83d9d83
Create Date: 2024-11-23 13:38:27.274141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08a84f398d83'
down_revision: Union[str, None] = '00fda83d9d83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('bank_user', 'phone',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_constraint('bank_user_phone_key', 'bank_user', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('bank_user_phone_key', 'bank_user', ['phone'])
    op.alter_column('bank_user', 'phone',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
