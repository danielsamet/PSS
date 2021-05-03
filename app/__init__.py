import os

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager

from app.main.phonemes.phoneme_map import generate_phoneme_map
from app.main.phonemes.utils import get_words
from app.config import Config

migrate = Migrate()
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config, skip_dir_building=False):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, config_class.MIGRATIONS_DIR)
    login.init_app(app)

    if not skip_dir_building:
        recording_dir = os.path.join("app", "static", "recording")
        if not os.path.isdir(recording_dir):
            os.mkdir(recording_dir)

    # DIR setup
    app.config["BASE_DIR"] = ""
    app.config["STATIC_DIR"] = os.path.join(app.config["BASE_DIR"], "static")
    app.config["USER_DIR_NAME"] = "user_data"
    app.config["USER_DIR"] = os.path.join(app.config["BASE_DIR"], app.config["USER_DIR_NAME"])

    app.phoneme_map = generate_phoneme_map(app.config["STATIC_DIR"])

    app.add_url_rule("/favicon", "favicon", lambda: redirect(url_for("static", filename="favicon/favicon.ico")))
    app.add_url_rule("/favicon-16x16", "favicon-16x16",
                     lambda: redirect(url_for("static", filename="favicon/favicon-16x16.png")))
    app.add_url_rule("/favicon-32x32", "favicon-32x32",
                     lambda: redirect(url_for("static", filename="favicon/favicon-32x32.png")))
    app.add_url_rule("/apple-touch-icon", "apple-touch-icon",
                     lambda: redirect(url_for("static", filename="favicon/apple-touch-icon.png")))
    app.add_url_rule("/site_webmanifest", "site_webmanifest",
                     lambda: redirect(url_for("static", filename="favicon/site.webmanifest")))

    from app.routes import bp as home_bp
    app.register_blueprint(home_bp)

    from app.auth.models import User
    UserManager(app, db, User)

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import bp as error_bp
    app.register_blueprint(error_bp)

    from app.main.routes import bp as main_bp
    app.register_blueprint(main_bp)

    @app.shell_context_processor  # adds automatic context to the shell
    def make_shell_context():
        from app.auth.models import User, Role
        from app.main.models import Phoneme, PhonemeExample, PhonemeRecording

        return dict(app=app, db=db,
                    User=User, Role=Role,
                    Phoneme=Phoneme, PhonemeExample=PhonemeExample, PhonemeRecording=PhonemeRecording)

    return app
