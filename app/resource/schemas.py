from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

def load_sql_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

CHECK_SPAM_VIOLATION_FN = PGFunction(
    schema="public",
    signature="check_spam_violation()",
    definition=load_sql_from_file('./app/resource/check_spam_violation.sql')
)

CHECK_SPAM_VIOLATION_TG = PGTrigger(
    schema="public",
    signature="trigger_spam_violation_check",
    on_entity="messages",
    is_constraint=False,
    definition=load_sql_from_file('./app/resource/trigger_spam_violation_check.sql'))

