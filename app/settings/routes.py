from . import settings_bp
from flask import render_template

@settings_bp.route("/settings")
def settings():
    return render_template("settings.html")