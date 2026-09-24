"""
Front-end preview routes only.
TODO (backend phase): replace placeholder data with calls into
app/controllers/*.py, which run raw SQL via app/models/*.py.
Per spec §6.3, keep dispatch here manual — no Flask blueprints/converters
beyond what's needed to preview these views.
"""
from flask import render_template, request, redirect, url_for, session

PLACEHOLDER_PHOTOS = [
    {"id": 1, "title": "Nile at Dusk", "author": "Amira K.", "user_id": 1},
    {"id": 2, "title": "Omdurman Market", "author": "Youssef T.", "user_id": 2},
    {"id": 3, "title": "Khartoum Skyline", "author": "Salma H.", "user_id": 3},
    {"id": 4, "title": "Old Bridge", "author": "Amira K.", "user_id": 1},
    {"id": 5, "title": "Coffee Corner", "author": "Mo Idris", "user_id": 4},
    {"id": 6, "title": "Desert Road", "author": "Salma H.", "user_id": 3},
]

PLACEHOLDER_COMMENTS = [
    {"who": "Youssef T.", "when": "2026-08-14 21:03", "text": "This is stunning, what camera?"},
    {"who": "Salma H.", "when": "2026-08-15 08:41", "text": "The light on the water 😍"},
]


def register_routes(app):

    @app.route("/")
    def home():
        stats = {"photos": 2480, "members": 612, "comments": 5109}
        return render_template("home.html", photos=PLACEHOLDER_PHOTOS, stats=stats)

    @app.route("/photos")
    def gallery():
        return render_template("photos/index.html", photos=PLACEHOLDER_PHOTOS)

    @app.route("/photo/<int:photo_id>")
    def photo_show(photo_id):
        photo = next((p for p in PLACEHOLDER_PHOTOS if p["id"] == photo_id), PLACEHOLDER_PHOTOS[0])
        photo = {**photo, "date": "2026-08-14", "description": "Taken from the Tuti bridge just after sunset."}
        return render_template("photos/show.html", photo=photo, comments=PLACEHOLDER_COMMENTS)

    @app.route("/photo/create")
    def photo_create():
        if not session.get("user"):
            return redirect(url_for("login"))
        return render_template("photos/create.html")

    @app.route("/photo/store", methods=["POST"])
    def photo_store():
        # TODO: PhotoController.store() — save file + insert row via raw SQL
        return redirect(url_for("gallery"))

    @app.route("/photo/<int:photo_id>/delete", methods=["POST"])
    def photo_delete(photo_id):
        # TODO: PhotoController.delete() — verify ownership, delete row + file
        return redirect(url_for("gallery"))

    @app.route("/photo/<int:photo_id>/comment", methods=["POST"])
    def comment_store(photo_id):
        # TODO: CommentController.store() — insert comment row
        return redirect(url_for("photo_show", photo_id=photo_id))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            # TODO: AuthController.login() — verify + set session + last_login cookie
            session["user"] = {"id": 1, "first_name": "Preview"}
            return redirect(url_for("home"))
        return render_template("auth/login.html")

    @app.route("/register", methods=["POST"])
    def register():
        # TODO: AuthController.register() — validate + hash + insert user
        return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))
