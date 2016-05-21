from flask import render_template, Flask, redirect, url_for, request, Response
import StringIO
from werkzeug import secure_filename
import JavaModule
import sys
import logging
import os
import json
import pandas as pd

ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze')
def analyze():
    try:
        return "TODO"
    except Exception as e:
        logging.error(e)
        return Response(status=500, mimetype='text/plain')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/scan_csv', methods=['POST'])
def scan_csv():
    file = request.files['file']
    if file and allowed_file(file.filename):
        results = JavaModule.scan_archive(file)
        upload_csv = StringIO.StringIO()
        pd.DataFrame(results).to_csv(upload_csv, index=False)
        print upload_csv.getvalue()
        return Response(upload_csv.getvalue(), mimetype='text/csv')
    return Response(status=500, mimetype='text/plain')


@app.route('/scan_json', methods=['POST'])
def scan_json():
    file = request.files['file']
    if file and allowed_file(file.filename):
        results = JavaModule.scan_archive(file)
        return Response(json.dumps(results), mimetype='text/json')
    return Response(status=500, mimetype='text/plain')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, handler=logging.StreamHandler(sys.stdout),
                        format='%(levelname)s - %(module)s - %(message)s')
    port = os.getenv('PORT', '5000')
    logging.info("Starting ephemerol web on port: %s", port)
    app.run(host='0.0.0.0', port=int(port))
