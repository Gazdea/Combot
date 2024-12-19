"""migration

Revision ID: 2e0bbc46afd9
Revises: 5727afe69c6a
Create Date: 2024-11-14 16:36:03.200888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic_utils.pg_trigger import PGTrigger
from sqlalchemy import text as sql_text

# revision identifiers, used by Alembic.
revision: str = '2e0bbc46afd9'
down_revision: Union[str, None] = '5727afe69c6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    public_messages_trigger_spam_violation_check = PGTrigger(
        schema="public",
        signature="trigger_spam_violation_check",
        on_entity="public.messages",
        is_constraint=False,
        definition='AFTER INSERT ON messages\nFOR EACH ROW\nEXECUTE FUNCTION check_spam_violation()'
    )
    op.create_entity(public_messages_trigger_spam_violation_check)

    public_chats_trigger_insert_roles_and_commands = PGTrigger(
        schema="public",
        signature="trigger_insert_roles_and_commands",
        on_entity="public.chats",
        is_constraint=False,
        definition='AFTER INSERT ON chats\nFOR EACH ROW\nEXECUTE FUNCTION insert_standard_roles_and_commands()'
    )
    op.create_entity(public_chats_trigger_insert_roles_and_commands)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    public_chats_trigger_insert_roles_and_commands = PGTrigger(
        schema="public",
        signature="trigger_insert_roles_and_commands",
        on_entity="public.chats",
        is_constraint=False,
        definition='AFTER INSERT ON chats\nFOR EACH ROW\nEXECUTE FUNCTION insert_standard_roles_and_commands()'
    )
    op.drop_entity(public_chats_trigger_insert_roles_and_commands)

    public_messages_trigger_spam_violation_check = PGTrigger(
        schema="public",
        signature="trigger_spam_violation_check",
        on_entity="public.messages",
        is_constraint=False,
        definition='AFTER INSERT ON messages\nFOR EACH ROW\nEXECUTE FUNCTION check_spam_violation()'
    )
    op.drop_entity(public_messages_trigger_spam_violation_check)

    # ### end Alembic commands ###