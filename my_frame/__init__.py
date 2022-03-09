import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

#app config, db, encryption, loginmanager
app = Flask(__name__)
app.config['SECRET_KEY'] = '93eafc13ec683d9b43358e5afc236714'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#app API
from my_frame.api import api_blueprint
app.register_blueprint(api_blueprint, url_prefix="/api/v1")

#user must be logged in to show page & styling it blue
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)

from my_frame import routes