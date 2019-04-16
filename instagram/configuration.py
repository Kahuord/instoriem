import os

import pathlib

from flask import Config


class CoreConfig(Config):
    SECRET_KEY = 'asdasdasd'
    UPLOADS_DIRECTORY = pathlib.Path(__file__).parent.parent / 'uploads'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(CoreConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instagram.db'


class HerokuConfig(CoreConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
