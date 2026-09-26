from app.config import get_connection

 #Return every photo with the uploader name new posts first
def get_all_photos():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT photos.id, photos.title, photos.file_name, photos.user_id,
                   users.first_name, users.last_name
            FROM photos
            JOIN users ON photos.user_id = users.id
            ORDER BY photos.date_time DESC """)
        result = cur.fetchall()
    conn.close()
    return result

#Return one photo with the uploader name or none
def get_photo(photo_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT photos.*, users.first_name, users.last_name
            FROM photos
            JOIN users ON photos.user_id = users.id
            WHERE photos.id = %s """, (photo_id,))
        result = cur.fetchone()
    conn.close()
    return result

 #Insert a new photo linking with the uploading user
def insert_photo(user_id, file_name, title, description):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO photos (user_id, file_name, title, description) VALUES (%s, %s, %s, %s)",
            (user_id, file_name, title, description)
        )
        conn.commit()
    conn.close()
 
 #Delete a photo by id caller is responsible for the ownership check
def delete_photo(photo_id):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM photos WHERE id = %s", (photo_id,))
        conn.commit()
    conn.close()