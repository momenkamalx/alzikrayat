from app.models.comment import insert_comment, get_comment, delete_comment as delete_comment_row

def store(photo_id, user_id, text):
    text = text.strip() if text else ""
    if not text or len(text) > 500:
        return False
    insert_comment(photo_id, user_id, text)
    return True

def delete(comment_id, user_id):
    comment = get_comment(comment_id)
    if comment and comment["user_id"] == user_id:
        delete_comment_row(comment_id)
        return True
    return False