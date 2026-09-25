import os
import uuid
from app.models.photo import insert_photo, get_photo, delete_photo as delete_photo_row

ALLOWED_EXT = {"jpg", "jpeg", "png"}
MAX_SIZE = 8 * 1024 * 1024  # 8MB
UPLOAD_DIR = os.path.join("app", "static", "uploads")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

def store(form, file, user_id):
    title = form.get("title", "").strip()
    if not title or len(title) > 200:
        return False, "Title is required (max 200 characters)."
    if not file or file.filename == "":
        return False, "Please choose a file."
    if not allowed_file(file.filename):
        return False, "Only JPEG or PNG files are allowed."

    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    if size > MAX_SIZE:
        return False, "File must be under 8MB."

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(UPLOAD_DIR, filename))
    insert_photo(user_id, filename, title, form.get("description", "").strip())
    return True, None

def delete(photo_id, user_id):
    photo = get_photo(photo_id)
    if photo and photo["user_id"] == user_id:
        path = os.path.join(UPLOAD_DIR, photo["file_name"])
        if os.path.exists(path):
            os.remove(path)
        delete_photo_row(photo_id)
        return True
    return False