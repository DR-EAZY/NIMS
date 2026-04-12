from . import ip_bp
from flask import render_template, request, redirect
from app import mysql


# ===================== MAIN IPAM DASHBOARD =====================
@ip_bp.route("/ip")
@ip_bp.route("/ip-management")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ip_addresses")
    data = cur.fetchall()

    ips = []
    for row in data:
        ips.append({
            "id": row[0],
            "ip_address": row[1],
            "device_name": row[2],
            "status": row[3]
        })

    # stats (NEW 🔥)
    total = len(ips)
    used = len([i for i in ips if i["status"] == "Used"])
    free = len([i for i in ips if i["status"] == "Free"])

    return render_template(
        "ip_management/index.html",
        ips=ips,
        total=total,
        used=used,
        free=free
    )


# ===================== ADD =====================
@ip_bp.route("/add-ip", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        ip = request.form["ip_address"]
        device = request.form["device_name"]
        status = request.form["status"]

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO ip_addresses (ip_address, device_name, status) VALUES (%s, %s, %s)",
            (ip, device, status)
        )
        mysql.connection.commit()

        return redirect("/ip-management")

    return render_template("ip_management/add.html")


# ===================== DELETE =====================
@ip_bp.route("/delete-ip/<int:id>")
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ip_addresses WHERE id=%s", (id,))
    mysql.connection.commit()

    return redirect("/ip-management")


# ===================== EDIT =====================
@ip_bp.route("/edit-ip/<int:id>", methods=["GET", "POST"])
def edit(id):
    cur = mysql.connection.cursor()

    if request.method == "POST":
        ip = request.form["ip_address"]
        device = request.form["device_name"]
        status = request.form["status"]

        cur.execute("""
            UPDATE ip_addresses
            SET ip_address=%s, device_name=%s, status=%s
            WHERE id=%s
        """, (ip, device, status, id))
        mysql.connection.commit()

        return redirect("/ip-management")

    cur.execute("SELECT * FROM ip_addresses WHERE id=%s", (id,))
    row = cur.fetchone()

    ip_data = {
        "id": row[0],
        "ip_address": row[1],
        "device_name": row[2],
        "status": row[3]
    }

    return render_template("ip_management/edit.html", ip_data=ip_data)