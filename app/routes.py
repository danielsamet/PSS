import base64
import binascii
import os

from flask import current_app, redirect, url_for, render_template, Blueprint, jsonify, request

from app import db
from app.models import PhonemeRecording, Phoneme

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
    return render_template("concatenation_setup.html", phonemes=Phoneme.query.all())


@bp.route('/ml_setup')
def ml_setup():
    return render_template("ml_setup.html")


@bp.route("/save_recording", methods=["POST"])
def save_recording():
    phoneme_id = request.form.get("phoneme_id", 0, int)
    phoneme = Phoneme.query.filter_by(id=phoneme_id).first()

    if not phoneme:
        return jsonify({"msg": "Unknown phoneme id supplied!"}), 400

    file_name = f"{phoneme.number}.{current_app.config.get('AUDIO_FILE_EXT')}"
    file_relative_address = "recording"
    file_address = os.path.join(current_app.config.get("STATIC_DIR"), file_relative_address, file_name)

    try:
        audio_stream = request.form.get("audio", "", str)
        audio_stream = audio_stream.replace(f"data:{current_app.config.get('AUDIO_MIME_TYPE')};base64,", "")
        audio_binary = base64.decodebytes(audio_stream.encode("utf-8"))
        with open(file_address, "wb") as file:
            file.write(audio_binary)

    except (OSError, binascii.Error):
        return jsonify({"msg": "Recording could not be saved successfully!"}), 400

    if not phoneme.recording:
        phoneme.recording = PhonemeRecording(file_relative_address, file_name)
    else:
        phoneme.recording.relative_dir = file_relative_address
        phoneme.recording.name = file_name
    db.session.commit()

    return jsonify({"msg": "Recording successfully saved!"}), 200
