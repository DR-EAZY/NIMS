from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # DATABASE CONFIG
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Adebisi2003$'
    app.config['MYSQL_DB'] = 'pynims'

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