from app.config import get_connection



#Return the user matching this email or None if no match

def find_by_email(email):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cur.fetchone()
    conn.close()
    return result

#Insert a new user password hash will already be bcrypt hashed

def create_user(first_name, last_name, email, password_hash):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, password_hash)
        )
        conn.commit()
    conn.close()
    
#Return the total number of registered users

def count_all_users():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS total FROM users")
        result = cur.fetchone()
    conn.close()
    return result["total"]

 #Return id/first name/last name for every registered user in alphabetical order

def get_all_users():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT id, first_name, last_name FROM users ORDER BY first_name")
        result = cur.fetchall()
    conn.close()
    return result