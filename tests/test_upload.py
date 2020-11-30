import io
import os

DEMO_CSV_FILE = 'docs/demo.csv'


def test_upload_text_stream(test_client):
    file_name = 'stream.txt'
    data = {
        'file': (io.BytesIO(b"lorem"), file_name)
    }
    response = test_client.post('/upload', data=data)
    assert response.status_code == 400


def test_upload_textfile(test_client):
    file = 'tests/stub/random-file.txt'

    data = {
        'file': (open(os.path.abspath(file), 'rb'), 'sample.txt')
    }
    response = test_client.post('/upload', data=data)
    assert response.status_code == 400


def test_upload_csvfile(test_client):
    file = DEMO_CSV_FILE

    data = {
        'file': (open(os.path.abspath(file), 'rb'), 'demo.csv')
    }
    response = test_client.post('/upload', data=data)
    assert response.status_code == 200
