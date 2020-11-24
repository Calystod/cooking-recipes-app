from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
import os

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLITE_URL']
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = os.environ['DEBUG_TB_INTERCEPT_REDIRECTS'] == "True"

    toolbar = DebugToolbarExtension(app)

    db.init_app(app)

    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from auth.auth import auth_bp
    app.register_blueprint(auth_bp)

    # blueprint for non-auth parts of app
    from user.user import user_bp
    app.register_blueprint(user_bp)

    return app