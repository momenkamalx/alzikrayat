from flask import render_template, request, redirect, session, flash
from app.core.router import Router
from app.controllers import auth_controller, photo_controller, comment_controller
from app.models.photo import get_all_photos, get_photo
from app.models.comment import get_comments_for_photo, count_all_comments
from app.models.user import count_all_users, get_all_users

router = Router()


#Take the photo data from the database and organize it into a dictionary
#format that the templates can use
def _map_photo(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "file_name": row["file_name"],
        "user_id": row["user_id"],
        "author": f'{row["first_name"]} {row["last_name"]}'
    }

#contain recent photos , about , site stats
def home():
    photos = [_map_photo(r) for r in get_all_photos()]
    stats = {"photos": len(photos), "members": count_all_users(), "comments": count_all_comments()}
    return render_template("home.html", photos=photos, stats=stats)

#every uploaded photo
def gallery():
    photos = [_map_photo(r) for r in get_all_photos()]
    return render_template("photos/index.html", photos=photos)

#photo detail page  image, metadata, comments, mention list
def photo_show(photo_id):
    photo_id = int(photo_id)
    row = get_photo(photo_id)
    if not row:
        return redirect("/photos")
    photo = {
        **_map_photo(row),
        "description": row["description"],
        "date": row["date_time"].strftime("%Y-%m-%d")
    }
    raw_comments = get_comments_for_photo(photo_id)
    comments = [
        {
            "id": c["id"],
            "user_id": c["user_id"],
            "who": f'{c["first_name"]} {c["last_name"]}',
            "when": c["date_time"].strftime("%Y-%m-%d %H:%M"),
            "text": c["comment"]
        }
        for c in raw_comments
    ]
    users = get_all_users()
    return render_template("photos/show.html", photo=photo, comments=comments, users=users)

#upload form page
def photo_create():
    if not session.get("user"):
        return redirect("/login")
    return render_template("photos/create.html")

#Handle the upload form submission via photo_controller.store
def photo_store():
    if not session.get("user"):
        return redirect("/login")
    file = request.files.get("photo")
    success, error = photo_controller.store(request.form, file, session["user"]["id"])
    if not success:
        flash(error)
        return redirect("/photo/create")
    return redirect("/photos")

#Handle the upload form submission via photo_controller.store
def photo_delete(photo_id):
    photo_id = int(photo_id)
    if session.get("user"):
        photo_controller.delete(photo_id, session["user"]["id"])
    return redirect("/photos")

#Handle a new comment submission via comment_controller.store
def comment_store(photo_id):
    photo_id = int(photo_id)
    if session.get("user"):
        comment_controller.store(photo_id, session["user"]["id"], request.form.get("comment", ""))
    return redirect(f"/photo/{photo_id}")

#Handle a comment delete request via comment_controller.delete
def comment_delete(comment_id):
    comment_id = int(comment_id)
    photo_id = request.form.get("photo_id", "")
    if session.get("user"):
        comment_controller.delete(comment_id, session["user"]["id"])
        return redirect(f"/photo/{photo_id}")
    return redirect("/login")

#GET: show login/register page POST: assign to auth_controller.login
def login():
    if request.method == "POST":
        return auth_controller.login(request.form)
    return render_template("auth/login.html")

#Handle the register form submission via auth_controller.register
def register():
    auth_controller.register(request.form)
    return redirect("/login")

#Clear the session and redirect to home
def logout():
    session.clear()
    return redirect("/")

#connect each URL to the function that handles it
router.add("GET", "/", home)
router.add("GET", "/photos", gallery)
router.add("GET", "/photo/create", photo_create)
router.add("POST", "/photo/store", photo_store)
router.add("GET", "/photo/{photo_id:int}", photo_show)
router.add("POST", "/photo/{photo_id:int}/delete", photo_delete)
router.add("POST", "/photo/{photo_id:int}/comment", comment_store)
router.add("POST", "/comment/{comment_id:int}/delete", comment_delete)
router.add("GET", "/login", login)
router.add("POST", "/login", login)
router.add("POST", "/register", register)
router.add("GET", "/logout", logout)

#Send every request to  router to find the correct function
def register_routes(app):
    @app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
    @app.route("/<path:path>", methods=["GET", "POST"])
    def dispatch(path):
        full_path = "/" + path
        result = router.dispatch(request.method, full_path)
        if result is None:
            return "Not Found", 404
        return result