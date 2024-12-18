"""migration

Revision ID: 5069b4886938
Revises: f2a91b7825ad
Create Date: 2024-11-18 15:51:52.095404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5069b4886938'
down_revision: Union[str, None] = 'f2a91b7825ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('commands', sa.Column('method_name', sa.Text(), nullable=True))
    op.drop_column('commands', 'command_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('commands', sa.Column('command_name', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('commands', 'method_name')
    # ### end Alembic commands ###
