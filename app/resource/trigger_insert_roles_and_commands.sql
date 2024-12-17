AFTER INSERT ON chats
FOR EACH ROW
EXECUTE FUNCTION insert_standard_roles_and_commands();