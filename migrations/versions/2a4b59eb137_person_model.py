"""Person model

Revision ID: 2a4b59eb137
Revises: None
Create Date: 2015-05-12 14:08:55.660475

"""

# revision identifiers, used by Alembic.
revision = '2a4b59eb137'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flapi_persons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('UNPAID', 'DISABLED', 'ACTIVE', 'DECEASED'), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('last_name', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('avatar', sa.String(length=128), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flapi_persons_email'), 'flapi_persons', ['email'], unique=True)
    op.create_index(op.f('ix_flapi_persons_status'), 'flapi_persons', ['status'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_flapi_persons_status'), table_name='flapi_persons')
    op.drop_index(op.f('ix_flapi_persons_email'), table_name='flapi_persons')
    op.drop_table('flapi_persons')
    ### end Alembic commands ###