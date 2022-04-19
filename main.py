from flask import Flask
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from database import helper
from model.user import User
import os

app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = os.environ['DEBUG_TB_INTERCEPT_REDIRECTS'] == "True"

toolbar = DebugToolbarExtension(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_email):
    print(user_email)
    # since the user_id is just the primary key of our user table, use it in the query for the user
    user_data = helper.get('users', {'email': user_email})
    if(user_data):
        return User(user_data)
    else:
        return ""

# blueprint for auth routes in our app
from auth.auth import auth_bp
app.register_blueprint(auth_bp)

# blueprint for non-auth parts of app
from user.user import user_bp
app.register_blueprint(user_bp)

# @todo Rewrite recipe part
from recipe.recipe import recipe_bp
app.register_blueprint(recipe_bp)