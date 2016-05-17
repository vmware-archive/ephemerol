from flask import render_template, Flask, redirect, url_for, session, request, Response
import os
import sys
import logging

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

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, handler=logging.StreamHandler(sys.stdout),
                        format='%(levelname)s - %(module)s - %(message)s')

    port = os.getenv('PORT', '5000')
    logging.info("Starting ephemerol web on port: %s", port)
    app.run(host='0.0.0.0', port=int(port))
