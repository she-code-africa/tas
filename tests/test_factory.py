from srv import create_app


def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_status(client):
    response = client.get("/status")
    assert response.data == b"OK!"
