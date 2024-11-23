"""init

Revision ID: 70d0010cd329
Revises: 
Create Date: 2024-11-23 04:11:03.681361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70d0010cd329'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklisttokens',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('expire', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blacklisttokens_id'), 'blacklisttokens', ['id'], unique=False)
    op.create_table('category',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('main_category', sa.Integer(), nullable=True),
    sa.Column('verbose_name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['main_category'], ['category.category_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('category_id')
    )
    op.create_table('organization',
    sa.Column('organization_uuid', sa.Uuid(), nullable=False),
    sa.Column('system_name', sa.String(length=255), nullable=False),
    sa.Column('verbose_name', sa.String(length=255), nullable=False),
    sa.Column('accreditation', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('organization_uuid'),
    sa.UniqueConstraint('system_name')
    )
    op.create_index(op.f('ix_organization_organization_uuid'), 'organization', ['organization_uuid'], unique=False)
    op.create_table('user',
    sa.Column('user_uuid', sa.Uuid(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=255), nullable=False),
    sa.Column('firstname', sa.String(length=255), nullable=False),
    sa.Column('middlename', sa.String(length=255), nullable=False),
    sa.Column('lastname', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('birthday', sa.String(length=255), nullable=False),
    sa.Column('gender', sa.String(length=255), nullable=False),
    sa.Column('account_status', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.PrimaryKeyConstraint('user_uuid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone')
    )
    op.create_index(op.f('ix_user_user_uuid'), 'user', ['user_uuid'], unique=False)
    op.create_table('service',
    sa.Column('service_uuid', sa.Uuid(), nullable=False),
    sa.Column('organization_name', sa.String(length=255), nullable=False),
    sa.Column('system_name', sa.String(length=255), nullable=False),
    sa.Column('verbose_name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['organization_name'], ['organization.system_name'], ),
    sa.PrimaryKeyConstraint('service_uuid', 'organization_name'),
    sa.UniqueConstraint('system_name')
    )
    op.create_index(op.f('ix_service_organization_name'), 'service', ['organization_name'], unique=False)
    op.create_index(op.f('ix_service_service_uuid'), 'service', ['service_uuid'], unique=False)
    op.create_table('wallet',
    sa.Column('wallet_uuid', sa.Uuid(), nullable=False),
    sa.Column('wallet_number', sa.String(length=255), nullable=False),
    sa.Column('user_uuid', sa.Uuid(), nullable=True),
    sa.Column('balance', sa.DECIMAL(), nullable=False),
    sa.Column('wallet_type', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.user_uuid'], ),
    sa.PrimaryKeyConstraint('wallet_uuid'),
    sa.UniqueConstraint('wallet_number')
    )
    op.create_index(op.f('ix_wallet_wallet_uuid'), 'wallet', ['wallet_uuid'], unique=False)
    op.create_table('card',
    sa.Column('card_uuid', sa.Uuid(), nullable=False),
    sa.Column('card_number', sa.String(length=255), nullable=False),
    sa.Column('wallet_number', sa.String(length=255), nullable=True),
    sa.Column('balance', sa.DECIMAL(), nullable=False),
    sa.Column('card_type', sa.String(length=255), nullable=False),
    sa.Column('expiration_date', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.ForeignKeyConstraint(['wallet_number'], ['wallet.wallet_number'], ),
    sa.PrimaryKeyConstraint('card_uuid'),
    sa.UniqueConstraint('card_number')
    )
    op.create_index(op.f('ix_card_card_uuid'), 'card', ['card_uuid'], unique=False)
    op.create_table('income_transaction',
    sa.Column('transaction_uuid', sa.Uuid(), nullable=False),
    sa.Column('category', sa.String(length=255), nullable=False),
    sa.Column('target_card', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.DECIMAL(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.ForeignKeyConstraint(['target_card'], ['card.card_number'], ),
    sa.PrimaryKeyConstraint('transaction_uuid')
    )
    op.create_index(op.f('ix_income_transaction_transaction_uuid'), 'income_transaction', ['transaction_uuid'], unique=False)
    op.create_table('transaction',
    sa.Column('transaction_uuid', sa.Uuid(), nullable=False),
    sa.Column('transaction_card_target', sa.String(length=255), nullable=False),
    sa.Column('transaction_source_card', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.DECIMAL(), nullable=False),
    sa.Column('transaction_type', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=False),
    sa.CheckConstraint('amount > 0'),
    sa.ForeignKeyConstraint(['transaction_card_target'], ['card.card_number'], ),
    sa.ForeignKeyConstraint(['transaction_source_card'], ['card.card_number'], ),
    sa.PrimaryKeyConstraint('transaction_uuid')
    )
    op.create_index(op.f('ix_transaction_transaction_uuid'), 'transaction', ['transaction_uuid'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_transaction_uuid'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_index(op.f('ix_income_transaction_transaction_uuid'), table_name='income_transaction')
    op.drop_table('income_transaction')
    op.drop_index(op.f('ix_card_card_uuid'), table_name='card')
    op.drop_table('card')
    op.drop_index(op.f('ix_wallet_wallet_uuid'), table_name='wallet')
    op.drop_table('wallet')
    op.drop_index(op.f('ix_service_service_uuid'), table_name='service')
    op.drop_index(op.f('ix_service_organization_name'), table_name='service')
    op.drop_table('service')
    op.drop_index(op.f('ix_user_user_uuid'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_organization_organization_uuid'), table_name='organization')
    op.drop_table('organization')
    op.drop_table('category')
    op.drop_index(op.f('ix_blacklisttokens_id'), table_name='blacklisttokens')
    op.drop_table('blacklisttokens')
    # ### end Alembic commands ###
