"""Adds test column

Revision ID: 36f061da40c4
Revises: ab82b388e513
Create Date: 2021-01-06 16:56:40.573732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36f061da40c4'
down_revision = 'ab82b388e513'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('student', sa.Column('wants_email', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('student', 'wants_email')
    # ### end Alembic commands ###
