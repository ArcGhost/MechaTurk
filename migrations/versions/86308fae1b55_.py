"""empty message

Revision ID: 86308fae1b55
Revises: f1803263824d
Create Date: 2016-03-26 23:49:03.388470

"""

# revision identifiers, used by Alembic.
revision = '86308fae1b55'
down_revision = 'f1803263824d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hit', sa.Column('school', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hit', 'school')
    ### end Alembic commands ###