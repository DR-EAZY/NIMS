from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import mysql
from . import auth_bp
from MySQLdb import IntegrityError


# REGISTER
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, hashed_password)
            )
            mysql.connection.commit()
            cur.close()

            return redirect("/login")

        except IntegrityError:
            return render_template("auth/register.html", error="Username already exists")

    return render_template("auth/register.html")


# LOGIN
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # If already logged in
    if session.get("user"):
        return redirect("/")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password):
            session["user"] = user[1]   # username
            return redirect("/")
        else:
            return render_template("auth/login.html", error="Invalid username or password")

    return render_template("auth/login.html")


# LOGOUT
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")