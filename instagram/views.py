import flask

from flask.views import MethodView

from flask_login import login_user

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from instagram.db import db
from instagram.models import User


def create_user(user_name, email, password):
    user = User(
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

        user = User.query.filter_by(email=email).first()

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
