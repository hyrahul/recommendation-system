"""phase_2_create_knowledge_video_permission_chat_tables

Revision ID: f1021e811a66
Revises: c6d680d20b38
Create Date: 2025-12-28 23:23:13.882538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1021e811a66'
down_revision: Union[str, Sequence[str], None] = 'c6d680d20b38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ---------- FAQ ----------
    op.create_table(
        "faq",
        sa.Column("faq_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
    )

    # ---------- QNA ----------
    op.create_table(
        "qna",
        sa.Column("qna_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=True),
    )

    # ---------- Permission Group ----------
    op.create_table(
        "permission_group",
        sa.Column("permission_grp_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=100), nullable=False),
    )

    # ---------- Permission Group User ----------
    op.create_table(
        "permission_group_user",
        sa.Column(
            "permission_grp_id",
            sa.BigInteger(),
            sa.ForeignKey("permission_group.permission_grp_id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )

    # ---------- Video ----------
    op.create_table(
        "video",
        sa.Column("video_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "lecture_id",
            sa.BigInteger(),
            sa.ForeignKey("lectures.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
    )

    # ---------- Video Student ----------
    op.create_table(
        "video_student",
        sa.Column(
            "video_id",
            sa.BigInteger(),
            sa.ForeignKey("video.video_id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("watched", sa.Boolean(), nullable=False),
    )

    # ---------- Chat Record ----------
    op.create_table(
        "chat_record",
        sa.Column("record_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("chat_title", sa.String(length=20), nullable=True),
        sa.Column("chat_summary", sa.String(length=200), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
    )

    # ---------- Chat Message ----------
    op.create_table(
        "chat_message",
        sa.Column("message_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "record_id",
            sa.BigInteger(),
            sa.ForeignKey("chat_record.record_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("sender", sa.String(length=20), nullable=False),
        sa.Column("message_text", sa.Text(), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("chat_message")
    op.drop_table("chat_record")
    op.drop_table("video_student")
    op.drop_table("video")
    op.drop_table("permission_group_user")
    op.drop_table("permission_group")
    op.drop_table("qna")
    op.drop_table("faq")
