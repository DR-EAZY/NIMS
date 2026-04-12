from . import devices_bp
from flask import render_template, request, redirect
from app import mysql


# ===================== READ =====================
@devices_bp.route("/devices")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM devices")

    columns = [col[0] for col in cur.description]  # ✅ get column names
    data = cur.fetchall()

    devices = []
    for row in data:
        devices.append(dict(zip(columns, row)))  # ✅ map correctly

    return render_template("devices/index.html", devices=devices)


# ===================== CREATE =====================
@devices_bp.route("/add-device", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        model = request.form["model"]
        mac = request.form["mac_address"]
        ip = request.form["ip_address"]
        location = request.form["location"]
        serial = request.form["serial_number"]
        type_ = request.form["type"]
        status = request.form["status"]

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO devices 
            (name, model, mac_address, ip_address, location, serial_number, type, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, model, mac, ip, location, serial, type_, status))
        mysql.connection.commit()

        return redirect("/devices")

    return render_template("devices/add.html")


# ===================== DELETE =====================
@devices_bp.route("/delete/<int:id>")
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM devices WHERE id=%s", (id,))
    mysql.connection.commit()

    return redirect("/devices")


# ===================== EDIT =====================
@devices_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    cur = mysql.connection.cursor()

    if request.method == "POST":
        name = request.form["name"]
        model = request.form["model"]
        mac = request.form["mac_address"]
        ip = request.form["ip_address"]
        location = request.form["location"]
        serial = request.form["serial_number"]
        type_ = request.form["type"]
        status = request.form["status"]

        cur.execute("""
            UPDATE devices 
            SET name=%s, model=%s, mac_address=%s, ip_address=%s, 
                location=%s, serial_number=%s, type=%s, status=%s
            WHERE id=%s
        """, (name, model, mac, ip, location, serial, type_, status, id))
        mysql.connection.commit()

        return redirect("/devices")

    # GET single device
    cur.execute("SELECT * FROM devices WHERE id=%s", (id,))
    
    columns = [col[0] for col in cur.description]  # ✅ FIX
    row = cur.fetchone()
    device = dict(zip(columns, row)) if row else None

    return render_template("devices/edit.html", device=device)