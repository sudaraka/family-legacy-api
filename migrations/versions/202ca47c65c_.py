"""empty message

Revision ID: 202ca47c65c
Revises: 2a4b59eb137
Create Date: 2015-05-20 11:58:42.085502

"""

# revision identifiers, used by Alembic.
revision = '202ca47c65c'
down_revision = '2a4b59eb137'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flapi_legacy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'LOCKED'), nullable=False),
    sa.Column('lock_date', sa.DateTime(), nullable=True),
    sa.Column('archive_hash', sa.String(length=40), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('caretaker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['caretaker_id'], ['flapi_persons.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['flapi_persons.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('owner_id')
    )
    op.create_index(op.f('ix_flapi_legacy_status'), 'flapi_legacy', ['status'], unique=False)
    op.create_table('flapi_legacy_members',
    sa.Column('legacy_id', sa.Integer(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['legacy_id'], ['flapi_legacy.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['flapi_persons.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flapi_legacy_members')
    op.drop_index(op.f('ix_flapi_legacy_status'), table_name='flapi_legacy')
    op.drop_table('flapi_legacy')
    ### end Alembic commands ###