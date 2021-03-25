import os

from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.phoneme_example_dict import phoneme_words
from app.utils import get_words
from config import Config

migrate = Migrate()
db = SQLAlchemy()


def create_app(config_class=Config, skip_dir_building=False):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, config_class.MIGRATIONS_DIR)

    if not skip_dir_building:
        recording_dir = os.path.join("app", "static", "recording")
        if not os.path.isdir(recording_dir):
            os.mkdir(recording_dir)

    app.words = get_words()

    app.add_url_rule("/favicon", "favicon", lambda: redirect(url_for("static", filename="favicon/favicon.ico")))
    app.add_url_rule("/favicon-16x16", "favicon-16x16",
                     lambda: redirect(url_for("static", filename="favicon/favicon-16x16.png")))
    app.add_url_rule("/favicon-32x32", "favicon-32x32",
                     lambda: redirect(url_for("static", filename="favicon/favicon-32x32.png")))
    app.add_url_rule("/apple-touch-icon", "apple-touch-icon",
                     lambda: redirect(url_for("static", filename="favicon/apple-touch-icon.png")))
    app.add_url_rule("/site_webmanifest", "site_webmanifest",
                     lambda: redirect(url_for("static", filename="favicon/site.webmanifest")))

    from app.routes import bp
    app.register_blueprint(bp)

    @app.shell_context_processor  # adds automatic context to the shell
    def make_shell_context():
        from app.models import Phoneme, PhonemeExample, PhonemeRecording

        return dict(app=app, db=db,
                    Phoneme=Phoneme, PhonemeExample=PhonemeExample, PhonemeRecording=PhonemeRecording)

    return app
