"""update_role_enum

Revision ID: 07f0ad6e20ac
Revises: 42edf6b1fee3
Create Date: 2025-09-27 09:06:07.304511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07f0ad6e20ac'
down_revision: Union[str, Sequence[str], None] = '42edf6b1fee3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


"""update_role_enum

Revision ID: 07f0ad6e20ac
Revises: 42edf6b1fee3
Create Date: 2025-09-27 09:06:07.304511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07f0ad6e20ac'
down_revision: Union[str, Sequence[str], None] = '42edf6b1fee3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("ALTER TYPE role RENAME TO role_old")
    op.execute("CREATE TYPE role AS ENUM ('USER', 'ADMIN')")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE role USING (role::text::role)")
    op.execute("DROP TYPE role_old")

def downgrade():
    op.execute("ALTER TYPE role RENAME TO role_old")
    op.execute("CREATE TYPE role AS ENUM ('user', 'ADMIN')")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE role USING (role::text::role)")
    op.execute("DROP TYPE role_old")