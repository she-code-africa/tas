import tempfile

from flask import Blueprint, request, abort, make_response, Response
from flask.helpers import send_file, send_from_directory
from werkzeug.utils import secure_filename

from srv import helper

bp = Blueprint("file", __name__)


@bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload csv record to parse and extract repo links"""
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    if file.content_type != 'text/csv':
        response = make_response("Only CSV file are allowed", 400)
        return response

    tempdir = tempfile.mkdtemp()
    file.filename = secure_filename(file.filename)

    response_filename = helper.async_csv_worker(file, tempdir)
    try:
        return send_from_directory(tempdir, filename=response_filename, as_attachment=True)
    except FileNotFoundError:
        abort(Response('broken file on server'))
    except Exception as e:
        abort(Response(str(e)))
