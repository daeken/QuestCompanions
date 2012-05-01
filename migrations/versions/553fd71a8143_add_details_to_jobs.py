"""Add details to jobs.

Revision ID: 553fd71a8143
Revises: 1e0eb70a64cc
Create Date: 2012-04-30 22:02:47.349000

"""

# revision identifiers, used by Alembic.
revision = '553fd71a8143'
down_revision = '1e0eb70a64cc'

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.add_column('Job', sa.Column('details', sa.Unicode))


def downgrade():
    pass
