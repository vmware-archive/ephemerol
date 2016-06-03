# ephemerol
A Cloud Native readiness scanner

## Installing
(Need to work on install script)

## Development
### Running Directly
This utility uses Flask to run.  Install Flask as follows:
```
pip install flask
```

You then need to set an environment variable to point to the main Flask app script:
#### Windows Commmand Prompt
```
set FLASK_APP=ephemerol\ephemerol-web.py
```
#### Windows Powershell
```
$env:FLASK_APP="ephemerol\ephemerol-web.py"
```
#### \*nix types
```
export FLASK_APP=ephemerol\ephemerol-web.py
```

Finally, run the app as follows to start the web UI:
```
flask run
```

### Testing
To run tests, make sure to install dependencies, and also install the project in editable mode.
```
pip install -r requirements.txt
pip install -e .
```

Then you can run all the tests with the `py.test` command at the root of the project.
