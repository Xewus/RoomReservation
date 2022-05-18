"""003 rename Resrvation fields

Revision ID: cacaf221b23b
Revises: 586024e13c4d
Create Date: 2022-05-18 16:24:31.397267

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'cacaf221b23b'
down_revision = '586024e13c4d'
branch_labels = None
depends_on = None


def upgrade():
    # writed by Xewus
    op.alter_column(
        table_name='reservation',
        column_name='from_reserve',
        new_column_name='start_time'
    )
    op.alter_column(
        table_name='reservation',
        column_name='to_reserve',
        new_column_name='end_time'
    )
    op.alter_column(
        table_name='reservation',
        column_name='meetingroom_id',
        new_column_name='room_id'
    )


def downgrade():
    # writed by Xewus
    op.alter_column(
        table_name='reservation',
        new_column_name='from_reserve',
        column_name='start_time'
    )
    op.alter_column(
        table_name='reservation',
        new_column_name='to_reserve',
        column_name='end_time'
    )
    op.alter_column(
        table_name='reservation',
        new_column_name='meetingroom_id',
        column_name='room_id'
    )
