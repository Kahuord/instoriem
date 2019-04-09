import flask

from instagram.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    photos = db.relationship('Photo', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    path = db.Column(db.String, unique=True, nullable=False)

    likes = db.relationship('Like', backref='photo', lazy=True)

    comments = db.relationship('Comment', backref='photo', lazy=True)

    def url(self):
        link = flask.url_for(
            endpoint='view-file',
            file_name=self.path,
        )

        return link

    def detail_url(self):
        link = flask.url_for(
            endpoint='photo-detail',
            photo_id=self.id,
        )

        return link

    def like_url(self):
        link = flask.url_for(
            endpoint='add-like',
            photo_id=self.id,
        )

        return link

    def comment_url(self):
        link = flask.url_for(
            endpoint='add-comment',
            photo_id=self.id,
        )

        return link


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)

    content = db.Column(db.String, nullable=False)
