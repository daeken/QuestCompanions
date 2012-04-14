"""Add more phone verification

Revision ID: 217a62fe41a4
Revises: 41f769217f5d
Create Date: 2012-04-13 00:51:01.297000

"""

# revision identifiers, used by Alembic.
revision = '217a62fe41a4'
down_revision = '41f769217f5d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('User', sa.Column('verification_code', sa.Integer()))
    op.add_column('User', sa.Column('verification_tries', sa.Integer()))


def downgrade():
    pass
