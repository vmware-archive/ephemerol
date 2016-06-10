from flask import render_template, Flask, request, Response, flash
import Scanner
import sys
import logging
import os

ALLOWED_EXTENSIONS = set(['zip', 'csv'])

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
            Scanner.load_rules(file)
            flash('CSV Scan Rules Loaded')
            return render_template('index.html')
    except:
        flash('CSV Rules Load Failed. Check Rules CSV file.')
        return render_template('index.html')

    try:
        if request.form.get('submitbtn') == 'zip_scan':
            results = Scanner.scan_archive(file)
            return render_template('report.html', results=results, filename=file.filename)
    except:
        flash('ZIP File Scan Failed.')
        return render_template('index.html')



@app.route('/scan/report', methods=['POST'])
def scan_report():
    file = request.files['file']
    if file and allowed_file(file.filename):
        results = Scanner.scan_archive(file)
        return render_template('report.html', results=results, filename=file.filename)
    return Response(status=500, mimetype='text/plain')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, handler=logging.StreamHandler(sys.stdout),
                        format='%(levelname)s - %(module)s - %(message)s')
    port = os.getenv('PORT', '5000')
    logging.info("Starting ephemerol web on port: %s", port)

    app.run(host='0.0.0.0', port=int(port))

