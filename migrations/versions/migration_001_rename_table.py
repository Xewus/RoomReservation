"""001 rename table

Revision ID: cce4a2afcf08
Revises: 551fdbedab78
Create Date: 2022-05-12 14:02:39.783884

"""
from alembic import op

revision = 'cce4a2afcf08'
down_revision = '551fdbedab78'
branch_labels = None
depends_on = None


def upgrade():
    # writed by Xewus
    op.rename_table('mettingroom', 'meetingroom')


def downgrade():
    # writed by Xewus
    op.rename_table('meetingroom', 'mettingroom')
