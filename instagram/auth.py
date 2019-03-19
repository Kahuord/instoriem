from flask_login import LoginManager

from instagram.models import User

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
