import base64
import os

from flask import current_app, redirect, url_for, render_template, Blueprint, jsonify, request

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


@bp.route("/save_recording", methods=["POST"])
def save_recording():
    with open(os.path.join(current_app.config.get("STATIC_DIR"), "recording", "test.mp3"), "wb") as file:
        file.write(
            base64.decodebytes(request.form.get("audio").replace("audio/x-mpeg-3;base64,", "").encode("utf-8"))
        )

    return jsonify(), 200
