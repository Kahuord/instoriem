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

    application.add_url_rule(
        rule='/<user_id>/',
        view_func=views.ProfilePhotos.as_view('profile-photos'),
    )

    application.add_url_rule(
        rule='/photo/<photo_id>/',
        view_func=views.DetailPhoto.as_view('photo-detail'),
    )

    application.add_url_rule(
        rule='/upload/',
        view_func=views.UploadPhoto.as_view('upload-photo'),
    )

    application.add_url_rule(
        rule='/file/<file_name>/',
        view_func=views.ViewFile.as_view('view-file'),
    )

    application.add_url_rule(
        rule='/add_like/<photo_id>/',
        view_func=views.AddLike.as_view('add-like'),
    )

    return application
