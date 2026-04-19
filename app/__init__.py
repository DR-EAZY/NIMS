from flask import Flask, session, redirect, request
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # SECRET KEY
    app.secret_key = "supersecretkey"

    # DATABASE CONFIG
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Adebisi2003$'
    app.config['MYSQL_DB'] = 'pynims'

    mysql.init_app(app)

    # LOGIN PROTECTION
    @app.before_request
    def require_login():
        allowed = ["/login", "/register", "/static"]

        if not session.get("user"):
            if not any(request.path.startswith(a) for a in allowed):
                return redirect("/login")

    # IMPORT BLUEPRINTS
    from .auth import auth_bp
    from .devices import devices_bp
    from .dashboard import dashboard_bp
    from .accounts import accounts_bp
    from .ip import ip_bp
    from .settings import settings_bp
    from .camera import camera_bp

    # REGISTER BLUEPRINTS
    app.register_blueprint(auth_bp)
    app.register_blueprint(devices_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(ip_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(camera_bp)

    return app