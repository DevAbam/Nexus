"""added event poster

Revision ID: 7285513e270d
Revises: cca09d036a0a
Create Date: 2025-12-14 22:20:40.863380
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "7285513e270d"
down_revision: Union[str, Sequence[str], None] = "cca09d036a0a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # ✅ Add poster column as NULLABLE (safe for existing rows)
    op.add_column(
        "tbl_events",
        sa.Column(
            "event_poster_url",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=True,  # changed to True
        ),
    )

    # ✅ Alter enum with USING to avoid cast error
    op.alter_column(
        "tbl_events",
        "event_tag",
        existing_type=sa.VARCHAR(),
        type_=sa.Enum(
            "MUSIC",
            "SPORTS",
            "BUSINESS",
            "EDUCATION",
            "RELIGION",
            "TECH",
            "ART",
            "FOOD",
            "COMMUNITY",
            name="eventcategory",
        ),
        postgresql_using="event_tag::eventcategory",  # key fix
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    # 🔁 Revert enum back to VARCHAR
    op.alter_column(
        "tbl_events",
        "event_tag",
        existing_type=sa.Enum(
            "MUSIC",
            "SPORTS",
            "BUSINESS",
            "EDUCATION",
            "RELIGION",
            "TECH",
            "ART",
            "FOOD",
            "COMMUNITY",
            name="eventcategory",
        ),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )

    # 🗑 Remove poster column
    op.drop_column("tbl_events", "event_poster_url")
