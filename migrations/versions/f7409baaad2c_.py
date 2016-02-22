"""empty message

Revision ID: f7409baaad2c
Revises: a99421b664f8
Create Date: 2016-02-18 14:36:58.926848

"""

# revision identifiers, used by Alembic.
revision = 'f7409baaad2c'
down_revision = 'a99421b664f8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('host_name', sa.String(length=128), nullable=True),
    sa.Column('event_name', sa.String(length=128), nullable=True),
    sa.Column('event_type', sa.String(length=128), nullable=True),
    sa.Column('on_campus', sa.Boolean(), nullable=True),
    sa.Column('virtual', sa.Boolean(), nullable=True),
    sa.Column('location', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('start_date', sa.String(length=128), nullable=True),
    sa.Column('end_date', sa.String(length=128), nullable=True),
    sa.Column('start_time', sa.String(length=128), nullable=True),
    sa.Column('end_time', sa.String(length=128), nullable=True),
    sa.Column('time_zone', sa.String(length=128), nullable=True),
    sa.Column('all_day', sa.Boolean(), nullable=True),
    sa.Column('general_pricing', sa.String(length=128), nullable=True),
    sa.Column('member_pricing', sa.String(length=128), nullable=True),
    sa.Column('non_member_pricing', sa.String(length=128), nullable=True),
    sa.Column('registration_req', sa.Boolean(), nullable=True),
    sa.Column('registration_url', sa.Text(), nullable=True),
    sa.Column('event_page_url', sa.Text(), nullable=True),
    sa.Column('hit_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['hit_id'], ['hit.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'hit', sa.Column('deadline', sa.Integer(), nullable=True))
    op.add_column(u'hit', sa.Column('school', sa.String(length=128), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'hit', 'school')
    op.drop_column(u'hit', 'deadline')
    op.drop_table('event')
    ### end Alembic commands ###
