import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User, Asset

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SECRET_KEY="test-secret",
    )

    with app.app_context():
        db.drop_all()     
        db.create_all()

        
        if not User.query.filter_by(username="admin").first():
            db.session.add(User(
                username="admin",
                role="admin",
                password=generate_password_hash("Password12345!")
            ))

        if not User.query.filter_by(username="alice").first():
            db.session.add(User(
                username="alice",
                role="user",
                password=generate_password_hash("Password12345!")
            ))

        if not Asset.query.filter_by(asset_tag="LAP-001").first():
            db.session.add(Asset(
                name="Dell Latitude",
                asset_tag="LAP-001",
                asset_type="Laptop",
                location="London"
            ))

        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

def login(client, username, password):
    return client.post("/auth/login", data={"username": username, "password": password}, follow_redirects=True)
