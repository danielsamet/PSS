import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    MIGRATIONS_DIR = "migrations_local"

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STATIC_DIR = os.path.join(basedir, "app", "static")
