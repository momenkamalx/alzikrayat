from flask import render_template, request, redirect, url_for, session, flash
from app.controllers import auth_controller, photo_controller, comment_controller
from app.models.photo import get_all_photos, get_photo
from app.models.comment import get_comments_for_photo, count_all_comments
from app.models.user import count_all_users,  get_all_users



def _map_photo(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "file_name": row["file_name"],
        "user_id": row["user_id"],
        "author": f'{row["first_name"]} {row["last_name"]}'
    }


def register_routes(app):

    @app.route("/")
    def home():
        photos = [_map_photo(r) for r in get_all_photos()]
        stats = {"photos": len(photos), "members": count_all_users(), "comments": count_all_comments()}
        return render_template("home.html", photos=photos, stats=stats)

    @app.route("/photos")
    def gallery():
        photos = [_map_photo(r) for r in get_all_photos()]
        return render_template("photos/index.html", photos=photos)

    @app.route("/photo/<int:photo_id>")
    def photo_show(photo_id):
        row = get_photo(photo_id)
        if not row:
            return redirect(url_for("gallery"))
        photo = {
            **_map_photo(row),
            "description": row["description"],
            "date": row["date_time"].strftime("%Y-%m-%d")
        }
        raw_comments = get_comments_for_photo(photo_id)
        print("DEBUG RAW:", raw_comments)
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

    @app.route("/photo/create")
    def photo_create():
        if not session.get("user"):
            return redirect(url_for("login"))
        return render_template("photos/create.html")

    @app.route("/photo/store", methods=["POST"])
    def photo_store():
        if not session.get("user"):
            return redirect(url_for("login"))
        file = request.files.get("photo")
        success, error = photo_controller.store(request.form, file, session["user"]["id"])
        if not success:
            flash(error)
            return redirect(url_for("photo_create"))
        return redirect(url_for("gallery"))

    @app.route("/photo/<int:photo_id>/delete", methods=["POST"])
    def photo_delete(photo_id):
        if session.get("user"):
            photo_controller.delete(photo_id, session["user"]["id"])
        return redirect(url_for("gallery"))

    @app.route("/photo/<int:photo_id>/comment", methods=["POST"])
    def comment_store(photo_id):
        if session.get("user"):
            comment_controller.store(photo_id, session["user"]["id"], request.form.get("comment", ""))
        return redirect(url_for("photo_show", photo_id=photo_id))

    @app.route("/comment/<int:comment_id>/delete", methods=["POST"])
    def comment_delete(comment_id):
        if session.get("user"):
            photo_id = request.form.get("photo_id")
            comment_controller.delete(comment_id, session["user"]["id"])
            return redirect(url_for("photo_show", photo_id=photo_id))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            return auth_controller.login(request.form)
        return render_template("auth/login.html")

    @app.route("/register", methods=["POST"])
    def register():
        auth_controller.register(request.form)
        return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))