"""phase1_core_learning_schema

Revision ID: c6d680d20b38
Revises: 
Create Date: 2025-12-27 13:05:48.879863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6d680d20b38'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('full_name', sa.String(length=200), nullable=False),
        sa.Column('affiliation', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "affiliation IN ('Korea', 'USA', 'China')",
            name='chk_user_affiliation'
        ),
        sa.UniqueConstraint('username')
    )

    # categories
    op.create_table(
        'categories',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('visibility', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "visibility IN ('Korea', 'USA', 'China', 'OverseasCommon')",
            name='chk_category_visibility'
        ),
        sa.UniqueConstraint('name')
    )

    # lectures
    op.create_table(
        'lectures',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(length=300), nullable=False),
        sa.Column('category_id', sa.BigInteger(), nullable=False),
        sa.Column('difficulty', sa.String(length=50), nullable=False),
        sa.Column(
            'is_searchable',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "difficulty IN ('Basic', 'Intermediate', 'Advanced')",
            name='chk_lecture_difficulty'
        ),
        sa.ForeignKeyConstraint(
            ['category_id'],
            ['categories.id'],
            ondelete='RESTRICT'
        ),
    )

    # lecture_prerequisites
    op.create_table(
        'lecture_prerequisites',
        sa.Column('lecture_id', sa.BigInteger(), nullable=False),
        sa.Column('prerequisite_lecture_id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['lecture_id'], ['lectures.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['prerequisite_lecture_id'], ['lectures.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint(
            'lecture_id',
            'prerequisite_lecture_id',
            name='pk_lecture_prerequisites'
        )
    )

    # lecture_students
    op.create_table(
        'lecture_students',
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('lecture_id', sa.BigInteger(), nullable=False),
        sa.Column('study_status', sa.String(length=50), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "study_status IN ('NotStarted', 'InProgress', 'Completed')",
            name='chk_study_status'
        ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['lecture_id'], ['lectures.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint(
            'user_id',
            'lecture_id',
            name='pk_lecture_students'
        )
    )


def downgrade() -> None:
    op.drop_table('lecture_students')
    op.drop_table('lecture_prerequisites')
    op.drop_table('lectures')
    op.drop_table('categories')
    op.drop_table('users')
