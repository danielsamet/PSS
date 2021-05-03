import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or '53ca58f0a19696a3dc36e52936d2413c698f6cca0ffc383444806ba8a17f05e331572'

    MIGRATIONS_DIR = "migrations_local"

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER_EMAIL_SENDER_EMAIL = "danielqmuniproject@gmail.com"
    USER_APP_NAME = "PSS"
    USER_COPYRIGHT_YEAR = 2021
    USER_CORPORATION_NAME = "ProjectDan"
    USER_UNAUTHENTICATED_ENDPOINT = 'app.index'

    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = "6LeYor0aAAAAAL6o9uRsj0a_phvd69lmemNxZalY"
    RECAPTCHA_PRIVATE_KEY = "6LeYor0aAAAAAM8OjLCBsghCerL5sDM4DgdE6WwA"
    RECAPTCHA_OPTIONS = {"theme": "dark"}

    AUDIO_MIME_TYPE = "audio/webm;codecs=opus"
    AUDIO_FILE_EXT = "webm"
