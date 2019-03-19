from flask import Config


class InstagramConfig(Config):
    SECRET_KEY = 'asdasdasd'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instagram.db'
