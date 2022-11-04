"""migration

Revision ID: 7c7eaa11a94a
Revises: 0c3d51b557ba
Create Date: 2022-11-04 23:38:17.881537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c7eaa11a94a'
down_revision = '0c3d51b557ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=64), nullable=True),
    sa.Column('secret_key', sa.String(length=260), nullable=True),
    sa.Column('profile_url', sa.String(length=260), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_secret_key'), 'users', ['secret_key'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('vaults',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('description', sa.String(length=240), nullable=True),
    sa.Column('icon_type', sa.String(length=260), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vaults_id'), 'vaults', ['id'], unique=False)
    op.create_index(op.f('ix_vaults_name'), 'vaults', ['name'], unique=False)
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('username', sa.String(length=40), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=260), nullable=True),
    sa.Column('description', sa.String(length=240), nullable=True),
    sa.Column('page_url', sa.String(length=260), nullable=True),
    sa.Column('icon_type', sa.String(length=260), nullable=True),
    sa.Column('vault_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['vault_id'], ['vaults.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_email'), 'accounts', ['email'], unique=False)
    op.create_index(op.f('ix_accounts_id'), 'accounts', ['id'], unique=False)
    op.create_index(op.f('ix_accounts_name'), 'accounts', ['name'], unique=False)
    op.create_index(op.f('ix_accounts_username'), 'accounts', ['username'], unique=False)
    op.create_table('cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('number', sa.String(length=40), nullable=True),
    sa.Column('type', sa.String(length=40), nullable=True),
    sa.Column('bank', sa.String(length=40), nullable=True),
    sa.Column('ccv', sa.String(length=10), nullable=True),
    sa.Column('expiration', sa.String(length=10), nullable=True),
    sa.Column('pin', sa.String(length=10), nullable=True),
    sa.Column('description', sa.String(length=240), nullable=True),
    sa.Column('vault_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['vault_id'], ['vaults.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cards_bank'), 'cards', ['bank'], unique=False)
    op.create_index(op.f('ix_cards_id'), 'cards', ['id'], unique=False)
    op.create_index(op.f('ix_cards_name'), 'cards', ['name'], unique=False)
    op.create_index(op.f('ix_cards_number'), 'cards', ['number'], unique=False)
    op.create_index(op.f('ix_cards_type'), 'cards', ['type'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cards_type'), table_name='cards')
    op.drop_index(op.f('ix_cards_number'), table_name='cards')
    op.drop_index(op.f('ix_cards_name'), table_name='cards')
    op.drop_index(op.f('ix_cards_id'), table_name='cards')
    op.drop_index(op.f('ix_cards_bank'), table_name='cards')
    op.drop_table('cards')
    op.drop_index(op.f('ix_accounts_username'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_name'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_id'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_email'), table_name='accounts')
    op.drop_table('accounts')
    op.drop_index(op.f('ix_vaults_name'), table_name='vaults')
    op.drop_index(op.f('ix_vaults_id'), table_name='vaults')
    op.drop_table('vaults')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_secret_key'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
