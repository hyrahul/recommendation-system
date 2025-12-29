"""add language_code to faq and qna

Revision ID: 82eb786f925d
Revises: f1021e811a66
Create Date: 2025-12-29 21:51:38.371378

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "82eb786f925d"
down_revision: Union[str, Sequence[str], None] = "f1021e811a66"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "qna",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("language_code", sa.String(length=10), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )

    op.add_column(
        "faq",
        sa.Column("language_code", sa.String(length=10), nullable=False),
    )
    op.add_column(
        "faq",
        sa.Column("is_active", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "faq",
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("faq", "created_at")
    op.drop_column("faq", "is_active")
    op.drop_column("faq", "language_code")
    op.drop_table("qna")
