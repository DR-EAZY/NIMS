from flask import render_template, request, redirect
from app import mysql
from . import settings_bp


@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():
    cur = mysql.connection.cursor()

    # SAVE SETTINGS
    if request.method == "POST":
        system_name = request.form["system_name"]
        admin_email = request.form["admin_email"]
        theme = request.form["theme"]
        notifications = 1 if request.form.get("notifications") else 0

        cur.execute("""
            UPDATE settings
            SET system_name=%s, admin_email=%s, theme=%s, notifications=%s
            WHERE id=1
        """, (system_name, admin_email, theme, notifications))

        mysql.connection.commit()
        cur.close()

        return redirect("/settings")

    # LOAD SETTINGS
    cur.execute("SELECT * FROM settings WHERE id=1")
    row = cur.fetchone()
    cur.close()

    settings_data = {
        "system_name": row[1],
        "admin_email": row[2],
        "theme": row[3],
        "notifications": row[4]
    }

    return render_template("settings.html", settings=settings_data)