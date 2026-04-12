from flask import Blueprint

ip_bp = Blueprint(
    "ip_management",
    __name__,
    template_folder="../templates/ip_management"
)

from . import routes