"""Fix Card model: tablename, FK, color, from_dict

Revision ID: 6b44d52ea4b9
Revises: 48b58eec7dc4
Create Date: 2025-06-26 06:55:24.075638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b44d52ea4b9'
down_revision = '48b58eec7dc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.add_column(sa.Column('card_color', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('card', schema=None) as batch_op:
        batch_op.drop_column('card_color')

    # ### end Alembic commands ###
