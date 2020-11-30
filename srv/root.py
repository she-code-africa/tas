from flask import Blueprint

bp = Blueprint("root", __name__)


@bp.route('/')
def index():
    """TAS Root Route"""
    return 'SCA Track Assessment Server'


@bp.route("/status")
def status():
    return "OK!"
