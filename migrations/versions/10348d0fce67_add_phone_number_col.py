"""Add phone number column

Revision ID: 10348d0fce67
Revises: None
Create Date: 2012-04-12 00:13:31.530000

"""

# revision identifiers, used by Alembic.
revision = '10348d0fce67'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('User', sa.Column('phone_number', sa.String()))


def downgrade():
    pass
