"""create tweet table

Revision ID: 6ce403259855
Revises: 
Create Date: 2021-08-12 18:20:39.288219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ce403259855'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tweet',
        sa.Column('id', sa.Integer, nullable=False, autoincrement=True, primary_key=True),
        sa.Column('tweet_id', sa.String(50), nullable=True),
        sa.Column('headline', sa.String(1000), nullable=True),
        sa.Column('content', sa.TEXT(60000), nullable=True),
        sa.Column('original_tweet', sa.String(1000), nullable=True),
        sa.Column('url', sa.String(1000), nullable=True),
        sa.Column('url_status', sa.String(10), nullable=True),
        sa.Column('status', sa.String(10), nullable=True),
    )
    op.execute('ALTER TABLE tweet AUTO_INCREMENT = 1;')



def downgrade():
    op.drop_table('tweet')
