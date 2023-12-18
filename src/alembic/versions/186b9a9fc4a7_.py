"""empty message

Revision ID: 186b9a9fc4a7
Revises: 
Create Date: 2023-12-18 13:01:44.087738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '186b9a9fc4a7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dataframe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('target', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dataframe_id'), 'dataframe', ['id'], unique=False)
    op.create_table('model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dataframe_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('type', sa.Enum('Linear', 'Tree', name='modelschoiceenum'), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['dataframe_id'], ['dataframe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_model_id'), 'model', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_model_id'), table_name='model')
    op.drop_table('model')
    op.drop_index(op.f('ix_dataframe_id'), table_name='dataframe')
    op.drop_table('dataframe')
    # ### end Alembic commands ###
