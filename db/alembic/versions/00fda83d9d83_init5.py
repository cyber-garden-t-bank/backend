"""init5

Revision ID: 00fda83d9d83
Revises: b1dc0524da6e
Create Date: 2024-11-23 13:26:23.353599

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00fda83d9d83'
down_revision: Union[str, None] = 'b1dc0524da6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bank_user', 'birthday')
    op.drop_column('bank_user', 'account_status')
    op.drop_column('bank_user', 'gender')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bank_user', sa.Column('gender', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('bank_user', sa.Column('account_status', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('bank_user', sa.Column('birthday', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
