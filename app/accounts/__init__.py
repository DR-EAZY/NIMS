from flask import Blueprint

accounts_bp = Blueprint(
    "accounts",
    __name__,
    template_folder="../templates/accounts"
)

from . import routes