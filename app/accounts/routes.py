from . import accounts_bp
from flask import render_template, request, redirect
from app import mysql


# READ
@accounts_bp.route("/accounts")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM accounts")
    data = cur.fetchall()

    accounts = []
    for row in data:
        accounts.append({
            "id": row[0],
            "service": row[1],
            "username": row[2],
            "password": row[3]
        })

    return render_template("accounts/index.html", accounts=accounts)


# CREATE
@accounts_bp.route("/add-account", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        service = request.form["service"]
        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO accounts (service, username, password) VALUES (%s, %s, %s)",
            (service, username, password)
        )
        mysql.connection.commit()

        return redirect("/accounts")

    return render_template("accounts/add.html")

# EDIT
@accounts_bp.route("/edit-account/<int:id>", methods=["GET", "POST"])
def edit(id):
    cur = mysql.connection.cursor()

    if request.method == "POST":
        service = request.form["service"]
        username = request.form["username"]
        password = request.form["password"]

        cur.execute("""
            UPDATE accounts 
            SET service=%s, username=%s, password=%s
            WHERE id=%s
        """, (service, username, password, id))
        mysql.connection.commit()

        return redirect("/accounts")

    # GET existing data
    cur.execute("SELECT * FROM accounts WHERE id=%s", (id,))
    row = cur.fetchone()

    account = {
        "id": row[0],
        "service": row[1],
        "username": row[2],
        "password": row[3]
    }

    return render_template("accounts/edit.html", account=account)

# DELETE
@accounts_bp.route("/delete-account/<int:id>")
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM accounts WHERE id=%s", (id,))
    mysql.connection.commit()

    return redirect("/accounts")