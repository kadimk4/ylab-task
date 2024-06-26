"""main

Revision ID: 6e69cceb4a6e
Revises: 
Create Date: 2024-01-21 18:02:30.776425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e69cceb4a6e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('submenu',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('menu_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('dishes',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.String(), nullable=False),
    sa.Column('submenu_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenu.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dishes')
    op.drop_table('submenu')
    op.drop_table('menu')
    # ### end Alembic commands ###
