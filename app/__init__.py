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
load_dotenv()

def create_app():
    app = Flask(__name__)
    #secret key, this should be randomised for production
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY',
        ''
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        ''
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

    # ensure database tables are created based on the current models
    # (SQLite won't create tables until we explicitly do so)
    with app.app_context():
        from . import models  # noqa: F401
        db.create_all()

    

    return app
