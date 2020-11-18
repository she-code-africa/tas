import tempfile

from flask import Blueprint, request, abort
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename

from srv import helper

bp = Blueprint("file", __name__)


@bp.route('/files/csv', methods=['POST'])
def upload_file():
    """Upload csv record to parse and extract repo links"""
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']
    if file.filename == '':
        return 'No selected file'

    tempdir = tempfile.mkdtemp()
    file.filename = secure_filename(file.filename)

    response_filename = helper.async_csv_worker(file, tempdir)
    try:
        return send_from_directory(tempdir, filename=response_filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
