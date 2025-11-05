"""update_test_user_uuids

Revision ID: cc83f56f9c70
Revises: 185dc935bd5d
Create Date: 2025-11-04 21:21:02.634871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc83f56f9c70'
down_revision: Union[str, Sequence[str], None] = '185dc935bd5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    
    # Update student external_id from old UUID to new UUID
    conn.execute(
        sa.text(
            'UPDATE "Students" SET external_id = :new_id WHERE external_id = :old_id'
        ),
        {
            'old_id': 'b7acb825-4e70-49e4-84a1-bf5dc7c8f509',
            'new_id': 'd03aa006-6f0b-4939-9287-753798b6d403'
        }
    )
    
    # Update teacher external_id from old UUID to new UUID
    conn.execute(
        sa.text(
            'UPDATE "Teachers" SET external_id = :new_id WHERE external_id = :old_id'
        ),
        {
            'old_id': 'fc6ac29a-b9dd-4b35-889f-2baff71f3be1',
            'new_id': '5a9cee80-7f1e-4bfb-8d4a-218128b3550f'
        }
    )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    
    # Revert student external_id to old UUID
    conn.execute(
        sa.text(
            'UPDATE "Students" SET external_id = :old_id WHERE external_id = :new_id'
        ),
        {
            'old_id': 'b7acb825-4e70-49e4-84a1-bf5dc7c8f509',
            'new_id': 'd03aa006-6f0b-4939-9287-753798b6d403'
        }
    )
    
    # Revert teacher external_id to old UUID
    conn.execute(
        sa.text(
            'UPDATE "Teachers" SET external_id = :old_id WHERE external_id = :new_id'
        ),
        {
            'old_id': 'fc6ac29a-b9dd-4b35-889f-2baff71f3be1',
            'new_id': '5a9cee80-7f1e-4bfb-8d4a-218128b3550f'
        }
    )
