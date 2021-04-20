from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from app.auth.forms import LoginForm

bp = Blueprint('app', __name__, url_prefix="/")


@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.synthesiser"))
    return render_template("index.html", form=LoginForm())
