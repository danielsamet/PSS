import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or '53ca58f0a19696a3dc36e52936d2413c698f6cca0ffc383444806ba8a17f05e331572'

    MIGRATIONS_DIR = "migrations_local"

    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STATIC_DIR = os.path.join(basedir, "", "static")

    USER_EMAIL_SENDER_EMAIL = "danielqmuniproject@gmail.com"

    AUDIO_MIME_TYPE = "audio/webm;codecs=opus"
    AUDIO_FILE_EXT = "webm"
