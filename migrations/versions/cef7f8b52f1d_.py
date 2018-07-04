"""empty message

Revision ID: cef7f8b52f1d
Revises: 3d28ba255156
Create Date: 2018-07-03 19:50:01.456182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cef7f8b52f1d'
down_revision = '3d28ba255156'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business', sa.Column('descriptio', sa.String(), nullable=False))
    op.drop_column('business', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business', sa.Column('description', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
    op.drop_column('business', 'descriptio')
    # ### end Alembic commands ###