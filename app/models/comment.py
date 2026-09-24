from app.config import get_connection

def get_comments_for_photo(photo_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT comments.comment, comments.date_time,
                   users.first_name, users.last_name
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE comments.photo_id = %s
            ORDER BY comments.date_time ASC
        """, (photo_id,))
        result = cur.fetchall()
    conn.close()
    return result

def insert_comment(photo_id, user_id, text):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO comments (photo_id, user_id, comment) VALUES (%s, %s, %s)",
            (photo_id, user_id, text)
        )
        conn.commit()
    conn.close()