"""your message

Revision ID: 187514c1b59b
Revises: 
Create Date: 2021-12-25 00:24:57.092832

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '187514c1b59b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=True),
                    sa.Column('hash_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.create_index(op.f('ix_user_hash_password'), 'user', ['hash_password'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)
    op.create_table('comment',
                    sa.Column('id', sa.Integer(), nullable=True),
                    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_comment_id'), 'comment', ['id'], unique=False)
    op.create_index(op.f('ix_comment_text'), 'comment', ['text'], unique=False)
    op.create_index(op.f('ix_comment_title'), 'comment', ['title'], unique=False)
    op.create_index(op.f('ix_comment_user_id'), 'comment', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comment_user_id'), table_name='comment')
    op.drop_index(op.f('ix_comment_title'), table_name='comment')
    op.drop_index(op.f('ix_comment_text'), table_name='comment')
    op.drop_index(op.f('ix_comment_id'), table_name='comment')
    op.drop_table('comment')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_hash_password'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
