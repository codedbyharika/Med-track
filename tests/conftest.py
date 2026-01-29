import pytest
from app import create_app, db, bcrypt
from app.models import User, Medicine, Appointment
from app.config import Config
from datetime import datetime

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client):
    # Register and login a user
    password = 'testpassword'
    hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    with client.application.app_context():
        user = User(email='test@example.com', password_hash=hashed, name='Test User')
        db.session.add(user)
        db.session.commit()
    
    client.post('/login', data={'email': 'test@example.com', 'password': password})
    return client
