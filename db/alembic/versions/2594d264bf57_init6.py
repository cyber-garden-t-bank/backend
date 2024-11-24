"""init6

Revision ID: 2594d264bf57
Revises: 79588e40299e
Create Date: 2024-11-24 06:07:15.018501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2594d264bf57'
down_revision: Union[str, None] = '79588e40299e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('income_transaction', sa.Column('transaction_user', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'income_transaction', 'bank_user', ['transaction_user'], ['user_uuid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'income_transaction', type_='foreignkey')
    op.drop_column('income_transaction', 'transaction_user')
    # ### end Alembic commands ###