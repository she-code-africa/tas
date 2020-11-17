import os
import tempfile

from flask import Blueprint
from flask import request
from werkzeug.utils import secure_filename

from srv import helper


bp = Blueprint("file", __name__)


@bp.route('/files/csv', methods=['POST'])
def upload_file():
    """Upload csv record to parse and extract repo links"""
    if 'file' not in request.files:
        return 'No file part'

    csv_fd, csv_path = tempfile.mkstemp()
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    file.filename = secure_filename(file.filename)
    file.save(csv_path)

    tempdir = os.path.dirname(csv_path)
    for s in helper.gen_get_link(csv_path):
        if s['repo'] == '':
            # TODO: properly handle missing repo links.
            continue
        command = f"--engine {str(s['track']).lower()} --repo {s['repo']} --dir {tempdir}"
        response = helper.invoke_runner(command)
        # TODO: handle response
        # if response == 1:
        #     print("failed")
        # else:
        #     print('passed')

    os.close(csv_fd)
    os.unlink(csv_path)

    return f'File: {file.filename} Uploaded.'
