#this is where we intialise the app and create the instance - assigning app variables
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

from dotenv import load_dotenv


def create_app():
    load_dotenv()
    app = Flask(__name__)
    #secret key, this should be randomised for production - loads from our .env file - if not found uses default value
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY',
        'dev-placeholder'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'sqlite:///assets.db'
    )

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    #our blueprints for that hold all our routes
    from .auth import auth as auth_blueprint
    from .routes import routes as routes_blueprint
    from .admin import admin as admin_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(routes_blueprint)
    app.register_blueprint(admin_blueprint)
    login_manager.login_view = "auth.login"
    

    return app
