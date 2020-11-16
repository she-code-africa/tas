import os
import tempfile

from flask import Blueprint
from flask import request
from werkzeug.utils import secure_filename

# from srv import helper


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
    file.save(os.path.join(csv_path))

    # for s in helper.gen_get_link(csv_path):
    #     command = f"--engine {s['track']} --repo {s['repo']} --dir {csv_path}"
    #     helper.invoke_runner(command)

    os.close(csv_fd)
    os.unlink(csv_path)

    return f'File: {file.filename} Uploaded.'
