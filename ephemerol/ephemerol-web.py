# Copyright (C) 2016-Present Pivotal Software, Inc. All rights reserved.
#
# This program and the accompanying materials are made available under
# the terms of the under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import render_template, Flask, request, Response, flash
import Scanner
import sys
import logging
import os
import tempfile

ALLOWED_EXTENSIONS = set(['zip', 'csv'])
UPLOAD_FOLDER = tempfile.gettempdir()

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    return render_template('report.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_rules():
    file = request.files['file']

    if file == False or allowed_file(file.filename) == False:
        flash('Invalid File Upload Attempt')
        return render_template('index.html')

    try:
        if request.form.get('submitbtn') == 'csv_load':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            Scanner.load_rules(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            flash('CSV Scan Rules Loaded')
            return render_template('index.html')
    except:
        flash('CSV Rules Load Failed. Check Rules CSV file.' + str(sys.exc_info()))
        return render_template('index.html')

    try:
        if request.form.get('submitbtn') == 'zip_scan':
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            results = Scanner.scan_archive(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return render_template('report.html', results=results, filename=file.filename)
    except:
        flash('ZIP File Scan Failed.' + str(sys.exc_info()))
        return render_template('index.html')

@app.route('/scan/report', methods=['POST'])
def scan_report():
    file = request.files['file']
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        results = Scanner.scan_archive(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return render_template('report.html', results=results, filename=file.filename)
    return Response(status=500, mimetype='text/plain')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, handler=logging.StreamHandler(sys.stdout),
                        format='%(levelname)s - %(module)s - %(message)s')
    port = os.getenv('PORT', '5000')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    logging.info("Starting ephemerol web on port: %s", port)

    app.run(host='0.0.0.0', port=int(port))

