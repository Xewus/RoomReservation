"""005 bind user_reserve

Revision ID: f056ecdd35a4
Revises: aa5969b22dc2
Create Date: 2022-05-21 11:11:23.312679

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy

# revision identifiers, used by Alembic.
revision = 'f056ecdd35a4'
down_revision = 'aa5969b22dc2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'user_id',
            fastapi_users_db_sqlalchemy.guid.GUID(),
            nullable=True
        ))
        batch_op.create_foreign_key(
            'fk_reservation_user_id_user', 'user', ['user_id'], ['id']
        )


def downgrade():
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_reservation_user_id_user', type_='foreignkey'
        )
        batch_op.drop_column('user_id')
