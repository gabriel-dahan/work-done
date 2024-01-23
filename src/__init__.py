from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from dotenv import dotenv_values

CONF = dotenv_values('.env')

__app = Flask(
    __name__,
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)
__app.url_map.strict_slashes = False

__app.config['SECRET_KEY'] = CONF['SECRET']

# DATABASE
__app.config['SQLALCHEMY_DATABASE_URI'] = CONF['DB_URI']
__app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
__db = SQLAlchemy(__app)

# LOGIN MANAGER
login_manager = LoginManager(__app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).first()

from .routes import *