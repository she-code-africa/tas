from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'SCA Accessment Server'


@app.route('/file/csv', methods=['POST'])
def csv_file():
    return 'CSV file uploaded'


if __name__ == '__main__':
    app.run()
