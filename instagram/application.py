import flask

from instagram import views
from instagram.db import db
from instagram.auth import login_manager


def create_application(configuration):
    application = flask.Flask(__name__)

    application.config.from_object(configuration)

    db.init_app(application)

    try:
        db.create_all(app=application)

    except:
        pass

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
        rule='/user/<user_id>/',
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

    application.add_url_rule(
        rule='/add_comment/<photo_id>/',
        view_func=views.AddComment.as_view('add-comment'),
    )

    return application
