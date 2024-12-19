AFTER INSERT ON messages
FOR EACH ROW
EXECUTE FUNCTION check_spam_violation();