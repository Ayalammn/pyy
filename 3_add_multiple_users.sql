CREATE OR REPLACE PROCEDURE add_multiple_users(users JSON)
LANGUAGE plpgsql
AS $$
DECLARE
    u JSON;
    incorrect_data JSONB := '[]'::JSONB;
BEGIN
    FOR u IN SELECT * FROM json_array_elements(users)
    LOOP
        IF (u->>'phone') ~ '^\d{10,}$' THEN
            IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = u->>'first_name') THEN
                UPDATE phonebook
                SET phone = u->>'phone'
                WHERE first_name = u->>'first_name';
            ELSE
                INSERT INTO phonebook(first_name, phone)
                VALUES (u->>'first_name', u->>'phone');
            END IF;
        ELSE
            incorrect_data := incorrect_data || u;
        END IF;
    END LOOP;
    
    RAISE NOTICE 'Incorrect data: %', incorrect_data;
END;
$$;
