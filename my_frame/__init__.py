from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from my_frame.config import Config

#app config, db, encryption, loginmanager
mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

#user must be logged in to show page & styling it blue
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from my_frame.api import api_blueprint
    from my_frame.posts.routes import posts
    from my_frame.users.routes import users
    from my_frame.main.routes import main

    #blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)

    return app