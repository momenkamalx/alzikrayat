from app.config import get_connection

 #Return every comment on one photo with the  commenter name oldest first
def get_comments_for_photo(photo_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT comments.id, comments.user_id, comments.comment, comments.date_time,
                   users.first_name, users.last_name
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE comments.photo_id = %s
            ORDER BY comments.date_time ASC
        """, (photo_id,))
        result = cur.fetchall()
    conn.close()
    return result

#Insert a new comment on the photo by the user
def insert_comment(photo_id, user_id, text):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO comments (photo_id, user_id, comment) VALUES (%s, %s, %s)",
            (photo_id, user_id, text)
        )
        conn.commit()
    conn.close()

#Return one comment's full row or none
def get_comment(comment_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM comments WHERE id = %s", (comment_id,))
        result = cur.fetchone()
    conn.close()
    return result

  #Return the total number of comments from all photos
def count_all_comments():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS total FROM comments")
        result = cur.fetchone()
    conn.close()
    return result["total"]

#Delete a comment by id Caller is responsible for the ownership check
def delete_comment(comment_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
        conn.commit()
    conn.close()
    
    