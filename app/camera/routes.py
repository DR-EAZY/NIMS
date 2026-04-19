from flask import render_template, request, redirect
from app import mysql
from . import camera_bp
from MySQLdb import IntegrityError


# VIEW ALL CAMERAS
@camera_bp.route("/camera")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cameras")
    data = cur.fetchall()
    cur.close()

    gti = [c for c in data if c[7] == "GTI"]
    five = [c for c in data if c[7] == "Five Continents"]

    return render_template("camera/index.html", gti=gti, five=five)


# ADD CAMERA
@camera_bp.route("/add-camera", methods=["GET", "POST"])
def add_camera():
    if request.method == "POST":
        try:
            cur = mysql.connection.cursor()

            cur.execute("""
                INSERT INTO cameras 
                (location, ip, serial_number, mac_address, password, status, category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                request.form["location"],
                request.form["ip"],
                request.form["serial_number"],
                request.form["mac_address"],
                request.form["password"],
                request.form["status"],
                request.form["category"]
            ))

            mysql.connection.commit()
            cur.close()

            return redirect("/camera")

        except IntegrityError:
            return "Error: Duplicate IP / MAC / Serial Number not allowed"

    return render_template("camera/add.html")
# DELETE CAMERA
@camera_bp.route("/delete-camera/<int:id>")
def delete_camera(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM cameras WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect("/camera")


# UPDATE CAMERA
@camera_bp.route("/update-camera/<int:id>", methods=["POST"])
def update_camera(id):
    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE cameras 
        SET location=%s, ip=%s, serial_number=%s, mac_address=%s, password=%s, status=%s, category=%s
        WHERE id=%s
    """, (
        request.form["location"],
        request.form["ip"],
        request.form["serial_number"],
        request.form["mac_address"],
        request.form["password"],
        request.form["status"],
        request.form["category"],
        id
    ))

    mysql.connection.commit()
    cur.close()

    return redirect("/camera")