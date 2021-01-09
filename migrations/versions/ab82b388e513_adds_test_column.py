"""Adds test column

Revision ID: ab82b388e513
Revises: a2b6b7110dfc
Create Date: 2021-01-06 16:55:08.764178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab82b388e513'
down_revision = 'a2b6b7110dfc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('wants_email', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student', 'wants_email')
    # ### end Alembic commands ###