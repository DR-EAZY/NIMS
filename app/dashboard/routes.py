from . import dashboard_bp
from flask import render_template

@dashboard_bp.route("/")
def dashboard():
    return render_template("dashboard.html")