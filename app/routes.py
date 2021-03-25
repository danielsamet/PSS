import base64
import binascii
import os

from flask import current_app, redirect, url_for, render_template, Blueprint, jsonify, request

from app import db
from app.models import PhonemeRecording

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
    symbol = request.form.get("phoneme_name", "", str)
    phoneme_num = request.form.get("phoneme_num", 0, int)

    if not 1 <= phoneme_num <= 84:
        return jsonify({"msg": "Phoneme number out of range."}), 400

    file_address = os.path.join(current_app.config.get("STATIC_DIR"), "recording", f"{phoneme_num}.mp3")

    try:
        audio_stream = request.form.get("audio", "", str).replace("audio/x-mpeg-3;base64,", "")
        audio_binary = base64.decodebytes(audio_stream.encode("utf-8"))
        with open(file_address, "wb") as file:
            file.write(audio_binary)

    except (OSError, binascii.Error):
        return jsonify({"msg": "Recording could not be saved successfully!"}), 400

    if not PhonemeRecording.query.filter_by(number=phoneme_num).first():
        db.session.add(PhonemeRecording(symbol, phoneme_num, file_address))
        db.session.commit()

    return jsonify({"msg": "Recording successfully saved!"}), 200
