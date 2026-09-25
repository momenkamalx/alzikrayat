import bcrypt
import re
from datetime import datetime
from flask import session, make_response, redirect, url_for, flash
from app.models.user import find_by_email, create_user

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _fail(message):
    flash(message)
    return redirect(url_for("login"))


def register(form):
    first_name = form.get("first_name", "").strip()
    last_name = form.get("last_name", "").strip()
    email = form.get("email", "").strip()
    password = form.get("password", "")

    if not first_name.isalpha() or len(first_name) > 50:
        return _fail("First name must be letters only")
    if not last_name.isalpha() or len(last_name) > 50:
        return _fail("Last name must be letters only")
    if not EMAIL_RE.match(email):
        return _fail("Enter a valid email address.")
    if len(password) < 8:
        return _fail("Password must be at least 8 characters.")
    if find_by_email(email):
        return _fail("An account with that email already exists.")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    create_user(first_name, last_name, email, hashed.decode())
    flash("Account created")
    return redirect(url_for("login"))


def login(form):
    email = form.get("email", "").strip()
    password = form.get("password", "")
    user = find_by_email(email)

    if not user or not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return _fail("Email or password is incorrect.")

    session["user"] = {"id": user["id"], "first_name": user["first_name"]}
    resp = make_response(redirect(url_for("home")))
    resp.set_cookie(
        "last_login",
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        max_age=7 * 24 * 60 * 60
    )
    return resp