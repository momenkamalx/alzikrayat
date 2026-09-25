
from flask import render_template, request, redirect, url_for, session
from app.controllers import auth_controller

PLACEHOLDER_PHOTOS = [
    {"id": 1, "title": "al-Nile", "author": "Ahmad", "user_id": 1},
    {"id": 2, "title": "Omdurman big Market", "author": "Ali", "user_id": 2},
]

PLACEHOLDER_COMMENTS = [
    {"photo_id": 2, "who": "Youssef", "when": "2026-08-14 21:03", "text": "This is beautifL"},
    {"photo_id": 1, "who": "Salma", "when": "2026-08-15 08:41", "text": "The light on the water"},
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
        comments = [c for c in PLACEHOLDER_COMMENTS if c["photo_id"] == photo_id]
        return render_template("photos/show.html", photo=photo, comments=comments)
    
    
    @app.route("/photo/create")
    def photo_create():
        if not session.get("user"):
            return redirect(url_for("login"))
        return render_template("photos/create.html")

    @app.route("/photo/store", methods=["POST"])
    def photo_store():
        
        return redirect(url_for("gallery"))

    @app.route("/photo/<int:photo_id>/delete", methods=["POST"])
    def photo_delete(photo_id):
        
        return redirect(url_for("gallery"))

    @app.route("/photo/<int:photo_id>/comment", methods=["POST"])
    def comment_store(photo_id):
        
        return redirect(url_for("photo_show", photo_id=photo_id))

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