import flask
from flask import *

app = Flask(__name__)

@app.route('/file_upload')
def file_upload(request_body)