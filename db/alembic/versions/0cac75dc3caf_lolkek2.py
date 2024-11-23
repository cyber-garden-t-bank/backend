"""lolkek2

Revision ID: 0cac75dc3caf
Revises: 58bffdfb08f4
Create Date: 2024-11-24 02:30:03.163677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0cac75dc3caf'
down_revision: Union[str, None] = '58bffdfb08f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('transaction_user', sa.Uuid(), nullable=False))
    op.add_column('transaction', sa.Column('category', sa.String(length=255), nullable=False))
    op.create_foreign_key(None, 'transaction', 'bank_user', ['transaction_user'], ['user_uuid'])
    op.drop_column('transaction', 'transaction_category')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('transaction_category', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'transaction', type_='foreignkey')
    op.drop_column('transaction', 'category')
    op.drop_column('transaction', 'transaction_user')
    # ### end Alembic commands ###
