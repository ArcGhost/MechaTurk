"""empty message

Revision ID: 24a2e44a3fc9
Revises: 9e6cca2de0f0
Create Date: 2016-01-31 18:32:39.781067

"""

# revision identifiers, used by Alembic.
revision = '24a2e44a3fc9'
down_revision = '9e6cca2de0f0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hit', sa.Column('assignment_id', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hit', 'assignment_id')
    ### end Alembic commands ###
