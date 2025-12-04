CREATE OR REPLACE FUNCTION get_phonebook_by_pattern(pattern TEXT)
RETURNS TABLE(
    id INT, 
    first_name VARCHAR, 
    last_name VARCHAR, 
    phone VARCHAR, 
    email VARCHAR, 
    created_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    WHERE first_name ILIKE '%' || pattern || '%'
       OR last_name ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$;
