# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "dev-placeholder"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL",
        "sqlite:///assets.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    # Register blueprints
    from .auth import auth as auth_blueprint
    from .routes import routes as routes_blueprint
    from .admin import admin as admin_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(routes_blueprint)
    app.register_blueprint(admin_blueprint)


    from .models import User

    with app.app_context():
        db.create_all()

        # Create demo admin if none exists
        if not User.query.filter_by(role="admin").first():
            admin = User(
                username="admin",
                role="admin",
                password=generate_password_hash("test123")
            )
            db.session.add(admin)
        
        if not User.query.filter_by(username="user").first():
            demo_user = User(
             username="user",
                role="user",
                password=generate_password_hash("test123")
            )
            db.session.add(demo_user)
            
            db.session.commit()

        

    return app
