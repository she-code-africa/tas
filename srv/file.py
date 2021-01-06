import tempfile
import json

from flask import Blueprint, request, abort, make_response, Response
from flask.helpers import send_file, send_from_directory
from werkzeug.utils import secure_filename

from srv import helper

bp = Blueprint("file", __name__)


@bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload csv record to parse and extract repo links"""
    response_filename = None
    tempdir = tempfile.mkdtemp()

    if request.content_type != 'application/json':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        if not ['application/pdf', 'text/csv'].__contains__(file.content_type):
            response = make_response("Only CSV file are allowed", 400)
            return response

        file.filename = secure_filename(file.filename)
        response_filename =  helper.async_csv_worker(file, tempdir)

    else:
        json_data = json.loads(request.data)['file']
        response_filename = helper.async_json_worker(json_data, tempdir)

    try:
        return send_from_directory(
            tempdir, filename=response_filename, as_attachment=True)
    except FileNotFoundError:
        abort(Response('broken file on server'))
    except Exception as e:
        abort(Response(str(e)))
