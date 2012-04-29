"""Add notification flags.

Revision ID: 1e0eb70a64cc
Revises: None
Create Date: 2012-04-29 15:07:38.378000

"""

# revision identifiers, used by Alembic.
revision = '1e0eb70a64cc'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.add_column('User', sa.Column('email_notifications', sa.Boolean))
	op.add_column('User', sa.Column('phone_notifications', sa.Boolean))


def downgrade():
	pass
