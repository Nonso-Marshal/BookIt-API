"""Update role enum to uppercase

Revision ID: f34b15b4e736
Revises: 07f0ad6e20ac
Create Date: 2025-09-29 07:51:33.731855

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f34b15b4e736'
down_revision: Union[str, Sequence[str], None] = '07f0ad6e20ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
