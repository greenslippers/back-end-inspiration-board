"""Add Board-Card relationship

Revision ID: 48b58eec7dc4
Revises: b117b029ab7f
Create Date: 2025-06-24 10:02:30.511217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48b58eec7dc4'
down_revision = 'b117b029ab7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('board_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'board', ['board_id'], ['board_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('board_id')

    # ### end Alembic commands ###
