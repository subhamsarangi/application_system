import pytest
from unittest.mock import patch
from app import app, db


@pytest.fixture
def mock_csrf():
    with patch("flask_wtf.csrf.validate_csrf", return_value=True):
        yield


@pytest.fixture
def test_app():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()

    yield app
    with app.app_context():
        db.drop_all()


def test_index(test_app):
    with test_app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200


def test_register_login_logout(test_app, mock_csrf):
    with test_app.test_client() as client:
        response = client.post(
            "/register",
            data=dict(email="testuser@example.com", password="testpassword"),
            follow_redirects=True,
        )
        assert b"Registration successful" in response.data

        response = client.post(
            "/login",
            data=dict(email="testuser@example.com", password="testpassword"),
            follow_redirects=True,
        )
        assert b"Logged in successfully" in response.data

        response = client.get("/logout", follow_redirects=True)
        assert b"Logged out successfully" in response.data
