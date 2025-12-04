import psycopg2
import json

conn = psycopg2.connect("dbname=lab11db user=postgres password=12345")
cur = conn.cursor()

# --- 1. Test pattern function ---
cur.execute("SELECT * FROM get_phonebook_by_pattern('Ali')")
print("Pattern search:", cur.fetchall())

# --- 2. Test add/update single user ---
cur.execute("CALL add_or_update_user('Sara', '87001112233')")

# --- 3. Test add multiple users ---
users_json = json.dumps([
    {"first_name": "John", "phone": "87003334455"},
    {"first_name": "Mary", "phone": "abc123"}  # incorrect
])
cur.execute(f"CALL add_multiple_users('{users_json}')")

# --- 4. Test pagination ---
cur.execute("SELECT * FROM get_phonebook_paginated(5,0)")
print("Pagination:", cur.fetchall())

# --- 5. Test delete ---
cur.execute("CALL delete_user(p_name := 'Sara')")

conn.commit()
cur.close()
conn.close()
