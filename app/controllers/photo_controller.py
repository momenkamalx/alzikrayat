import os
import uuid
from app.models.photo import insert_photo, get_photo, delete_photo as delete_photo_row

ALLOWED_EXT = {"jpg", "jpeg", "png"}
UPLOAD_DIR = os.path.join("app", "static", "uploads")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def store(form, file, user_id):
    if not file or file.filename == "" or not allowed_file(file.filename):
        return False
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(UPLOAD_DIR, filename))
    insert_photo(user_id, filename, form["title"], form.get("description", ""))
    return True

def delete(photo_id, user_id):
    photo = get_photo(photo_id)
    if photo and photo["user_id"] == user_id:
        path = os.path.join(UPLOAD_DIR, photo["file_name"])
        if os.path.exists(path):
            os.remove(path)
        delete_photo_row(photo_id)
        return True
    return False