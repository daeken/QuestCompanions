"""Add phone verification

Revision ID: 41f769217f5d
Revises: 10348d0fce67
Create Date: 2012-04-13 00:21:48.898000

"""

# revision identifiers, used by Alembic.
revision = '41f769217f5d'
down_revision = '10348d0fce67'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('User', sa.Column('phone_verified', sa.Boolean()))


def downgrade():
    op.delete_column('User', sa.Column('phone_number', sa.String()))
