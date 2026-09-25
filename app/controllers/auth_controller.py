import bcrypt
from datetime import datetime
from flask import session, make_response, redirect, url_for, flash
from app.models.user import find_by_email, create_user

def register(form):
    hashed = bcrypt.hashpw(form["password"].encode(), bcrypt.gensalt())
    create_user(form["first_name"], form["last_name"], form["email"], hashed.decode())

def login(form):
    user = find_by_email(form["email"])
    if user and bcrypt.checkpw(form["password"].encode(), user["password"].encode()):
        session["user"] = {"id": user["id"], "first_name": user["first_name"]}
        resp = make_response(redirect(url_for("home")))
        resp.set_cookie(
            "last_login",
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            max_age=7 * 24 * 60 * 60
        )
        return resp
    flash("Email or password is incorrect.")
    return redirect(url_for("login"))