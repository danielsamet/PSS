from flask import Blueprint, render_template

bp = Blueprint('app', __name__, url_prefix="/")


@bp.route('/')
@bp.route('/index')
def index():
    return render_template("index.html")
