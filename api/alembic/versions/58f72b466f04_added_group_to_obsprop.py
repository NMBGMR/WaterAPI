"""added group to obsprop

Revision ID: 58f72b466f04
Revises: a3c23fdd2520
Create Date: 2022-11-21 21:09:10.990785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "58f72b466f04"
down_revision = "a3c23fdd2520"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("ObservedProperty", sa.Column("group", sa.String))


def downgrade() -> None:
    op.drop_colum("ObservedProperty", "group")
