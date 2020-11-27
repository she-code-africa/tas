import pytest

from flask import Flask

from srv import create_app


@pytest.fixture
def app() -> Flask:
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app) -> Flask.test_client:
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()
