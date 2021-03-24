from flask import current_app, redirect, url_for, render_template, Blueprint

bp = Blueprint('main', __name__, url_prefix="/")


@bp.route('/')
@bp.route('/index')
def index():
    return redirect(url_for("main.synthesiser"))


@bp.route('/synthesiser')
def synthesiser():
    return render_template("synthesiser.html")


@bp.route('/concatenation_setup')
def concatenation_setup():
    return render_template("concatenation_setup.html", phoneme_dict=current_app.phoneme_dict)


@bp.route('/ml_setup')
def ml_setup():
    return render_template("ml_setup.html")
