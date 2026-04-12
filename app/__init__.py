from flask import Flask
from flask_mysqldb import MySQL
import os

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # DATABASE CONFIG
    MYSQL_HOST = os.getenv("mysql.railway.internal")
    MYSQL_USER = os.getenv("root")
    MYSQL_PASSWORD = os.getenv("pvJtsVUNnAqATvfhANmTGPqcsgoompwp")
    MYSQL_DB = os.getenv("railway")
    MYSQL_PORT = int(os.getenv("3306"))

    mysql.init_app(app)

    from .devices import devices_bp
    from .dashboard import dashboard_bp
    from .accounts import accounts_bp
    from .ip import ip_bp
    from .settings import settings_bp

    app.register_blueprint(devices_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(ip_bp)
    app.register_blueprint(settings_bp)

    return app