"""add user roles enum

Revision ID: 9ad5e94ec25a
Revises: b5ef4ecfdb64
Create Date: 2026-07-31 04:38:34.417254

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9ad5e94ec25a"
down_revision: Union[str, Sequence[str], None] = "b5ef4ecfdb64"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE userrole AS ENUM ('admin', 'user')")
    op.alter_column(
        "users",
        "role",
        existing_type=sa.VARCHAR(),
        type_=sa.Enum("admin", "user", name="userrole"),
        existing_nullable=False,
        postgresql_using="role::userrole",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users",
        "role",
        existing_type=sa.Enum("admin", "user", name="userrole"),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.execute("DROP TYPE IF EXISTS userrole")
