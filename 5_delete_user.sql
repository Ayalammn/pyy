CREATE OR REPLACE PROCEDURE delete_user(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE (p_name IS NOT NULL AND first_name = p_name)
       OR (p_phone IS NOT NULL AND phone = p_phone);
END;
$$;
