import flask

from instagram import views
from instagram.db import db
from instagram.auth import login_manager
from instagram.configuration import InstagramConfig


def create_application(configuration_class=InstagramConfig):
    application = flask.Flask(__name__)

    application.config.from_object(configuration_class)

    db.init_app(application)

    db.create_all(app=application)

    login_manager.init_app(application)

    application.add_url_rule(
        rule='/registration/',
        view_func=views.UserRegistrationView.as_view('registration'),
    )

    application.add_url_rule(
        rule='/login/',
        view_func=views.UserLoginView.as_view('login'),
    )

    return application
