import flask

from flask.views import MethodView

from flask_login import (
    login_user,
    current_user,
    login_required,
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from instagram.db import db

from instagram import models


def create_user(user_name, email, password):
    user = models.User(
        username=user_name,
        email=email,
        password=password
    )

    db.session.add(user)
    db.session.commit()


class UserRegistrationView(MethodView):
    def get(self):
        return flask.render_template('registration.html')

    def post(self):
        user_name = flask.request.form['user_name']
        email = flask.request.form['email']
        password = flask.request.form['password']

        hashed_password = generate_password_hash(password)

        create_user(
            user_name=user_name,
            email=email,
            password=hashed_password,
        )

        return f'user_name: {user_name} email: {email} password: {hashed_password}'


class UserLoginView(MethodView):
    def get(self):
        return flask.render_template('login.html')

    def post(self):
        email = flask.request.form['email']
        password = flask.request.form['password']

        user = models.User.query.filter_by(email=email).first()

        logged_in = False

        if user:
            is_correct = check_password_hash(
                pwhash=user.password,
                password=password,
            )

            if is_correct:
                login_user(user)

                logged_in = True

        if logged_in:
            return 'Logged in'

        return 'Failed to log in'


class ProfilePhotos(MethodView):
    def get(self, user_id):
        user = models.User.query.get(user_id)

        if user is None:
            return 'Profile not found', 404

        return flask.render_template('profile_photos.html', photos=user.photos)


class DetailPhoto(MethodView):
    def get(self, photo_id):
        photo = models.Photo.query.get(photo_id)

        return flask.render_template(
            template_name_or_list='photo.html',
            photo=photo,
        )


class UploadPhoto(MethodView):
    decorators = [
        login_required,
    ]

    def get(self):
        return flask.render_template('upload_photo.html')

    def post(self):
        file = flask.request.files['photo']

        file_name = flask.current_app.config['UPLOADS_DIRECTORY'] / file.filename

        file.save(str(file_name))

        photo = models.Photo(
            path=file.filename,
            user_id=current_user.id,
        )

        db.session.add(photo)
        db.session.commit()

        return 'ok'


class ViewFile(MethodView):
    def get(self, file_name):
        uploads_directory = str(flask.current_app.config['UPLOADS_DIRECTORY'])

        return flask.send_from_directory(uploads_directory, file_name)


class AddLike(MethodView):
    def post(self, photo_id):
        already_liked = models.Like.query.filter(
            models.Like.user_id == current_user.id,
            models.Like.photo_id == photo_id,
        ).count()

        if already_liked:
            return 'Sorry, we can not accept your like more than 1'

        like = models.Like(
            user_id=current_user.id,
            photo_id=photo_id,
        )

        db.session.add(like)
        db.session.commit()

        photo = models.Photo.query.get(photo_id)

        redirect_url = flask.url_for(
            endpoint='profile-photos',
            user_id=photo.user_id,
        )

        return flask.redirect(redirect_url)


class AddComment(MethodView):
    def post(self, photo_id):
        comment = models.Comment(
            user_id=current_user.id,
            photo_id=photo_id,
            content=flask.request.form['content'],
        )

        db.session.add(comment)
        db.session.commit()

        redirect_url = flask.url_for(
            endpoint='photo-detail',
            photo_id=photo_id,
        )

        return flask.redirect(redirect_url)
