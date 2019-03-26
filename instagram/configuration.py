import pathlib

from flask import Config


class InstagramConfig(Config):
    SECRET_KEY = 'asdasdasd'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instagram.db'

    UPLOADS_DIRECTORY = pathlib.Path(__file__).parent.parent / 'uploads'
