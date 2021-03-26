import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    MIGRATIONS_DIR = "migrations_local"

    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STATIC_DIR = os.path.join(basedir, "app", "static")

    AUDIO_MIME_TYPE = "audio/wav"
    AUDIO_FILE_EXT = "wav"
