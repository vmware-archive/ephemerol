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
from flask_cors import cross_origin
from Models import JSONEncoderModels
import Scanner
import sys
import logging
import os
import tempfile
import json

ALLOWED_EXTENSIONS = set(['zip', 'yml'])
UPLOAD_FOLDER = tempfile.gettempdir()

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def root():
    return app.send_static_file('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/scan', methods=['POST'])
@cross_origin()
def scan():
    file = request.files['file']
    if file == False or allowed_file(file.filename) == False:
        return Response(status=500, mimetype='application/json')

    try:
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        if (len(Scanner.rulebase) == 0):
            Scanner.load_yaml_rules(os.path.join(app.static_folder, 'default-rulebase.yml'))

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        results = Scanner.scan_archive(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return Response(json.dumps(results, cls=JSONEncoderModels), mimetype='application/json')

    except Exception as e:
        logging.error(e)
        return Response(status=500, mimetype='application/json')


@app.route('/load_rules', methods=['POST'])
@cross_origin()
def load_rules():

    file = request.files['file']
    if file == False or allowed_file(file.filename) == False:
        return Response(status=500, mimetype='application/json')

    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        Scanner.load_yaml_rules(file_path)
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        logging.error(e)
        return Response(status=500, mimetype='application/json')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, handler=logging.StreamHandler(sys.stdout),
                        format='%(levelname)s - %(module)s - %(message)s')
    port = os.getenv('PORT', '5000')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    logging.info("Starting ephemerol web on port: %s", port)

    app.run(host='0.0.0.0', port=int(port))
