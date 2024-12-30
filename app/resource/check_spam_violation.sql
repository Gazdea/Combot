RETURNS TRIGGER AS $$
DECLARE
    mute_duration FLOAT;
    max_messages INT;
    time_window INT;
    last_message_time TIMESTAMP;
BEGIN
    SELECT spam_mute_time, spam_message, spam_time
    INTO mute_duration, max_messages, time_window
    FROM chats
    WHERE id = NEW.chat_id;

    SELECT MAX(date) INTO last_message_time
    FROM messages
    WHERE user_id = NEW.user_id
    AND chat_id = NEW.chat_id;

    IF (SELECT COUNT(*) FROM messages
        WHERE user_id = NEW.user_id
          AND chat_id = NEW.chat_id
          AND date > (last_message_time - INTERVAL '1 second' * time_window)) >= max_messages THEN

        INSERT INTO muted_users (user_id, chat_id, time_end, reason)
        VALUES (NEW.user_id, NEW.chat_id, last_message_time + INTERVAL '1 minute' * mute_duration, 'Spamming');
    END IF;

    RETURN NEW;
END;
$$; LANGUAGE plpgsql;

