"""renamed event_id fk to event_uid

Revision ID: d3c5bf0d642e
Revises: ca4780a29a8e
Create Date: 2025-11-30 23:27:13.828752

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "d3c5bf0d642e"
down_revision: Union[str, Sequence[str], None] = "ca4780a29a8e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Rename the column event_id → event_uid
    op.alter_column("tbl_tickets", "event_id", new_column_name="event_uid")


def downgrade():
    # Rename back if rolling back
    op.alter_column("tbl_tickets", "event_uid", new_column_name="event_id")
