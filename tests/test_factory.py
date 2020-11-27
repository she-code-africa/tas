from srv import create_app


def test_config():
    """Test create_app without passing test config."""
    assert not create_app().testing
    assert create_app('testing').testing


def test_status(test_client):
    response = test_client.get("/status")
    assert response.data == b"OK!"


def test_index_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert response.data == b"SCA Track Assessment Server"
