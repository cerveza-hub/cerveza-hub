"""Merge multiple heads

Revision ID: 031ff6b93d73
Revises: 36fefc317ad0, 9f530c2a21a5
Create Date: 2025-12-02 08:49:33.099743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '031ff6b93d73'
down_revision = ('36fefc317ad0', '9f530c2a21a5')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
