from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from .databases import UsersDatabase
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)

db = UsersDatabase("users.db")
db.create_table()
db.close_connection()


@auth.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password")
        password2 = request.form.get("password1")
        db = UsersDatabase("users.db")
        if db.get_user_by_email(email):
            flash("Email currently in use", category="error")
        elif db.get_user_by_username(username):
            flash("Username currently in use", category="error")
        elif password1 != password2:
            flash("Passwords do not match", category="error")
        elif len(username) < 2:
            flash("Length of username must be at least 2 characters!", category="error")
        elif len(password1) < 6:
            flash("Length of password must be at least 6 characters!", category="error")
        elif len(email) < 6:
            flash("Length of email must be at least 6 characters!", category="error")
        else:
            db.add_user(
                username, generate_password_hash(password1, "sha256"), email, "", 0
            )
            session["current_user"] = db.get_user_by_username(username)[0]
            db.close_connection()
            flash("User created successfully", category="success")
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", signed_in=session.get("current_user"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        db = UsersDatabase("users.db")
        user = db.get_user_by_email(email)
        db.close_connection()
        if user:
            if check_password_hash(user[2], password):
                flash("Logged in!", category="success")
                session["current_user"] = user[0]
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("Invalid email", category="error")
    return render_template("login.html", signed_in=session.get("current_user"))


@auth.route("/logout")
def logout():
    session["current_user"] = None
    return redirect(url_for("views.home"))
