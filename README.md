# ephemerol
A Cloud Native readiness scanner that has configurable rules for Java, .NET and other cloud native application types.
[![Build Status](https://travis-ci.org/Pivotal-Field-Engineering/ephemerol.png?branch=master)](https://travis-ci.org/Pivotal-Field-Engineering/ephemerol)

## Requirements
Python 2.7.9

## Development
### Run Web Application Locally
Run the script as follows to get information on how to invoke it:
```
cd ./ephemerol
pip install -r requirements.txt
python ./ephemerol-web.py

```

### Testing
To run tests, make sure to install dependencies, then you can run all the tests with the `py.test` command at the root of the project.
```
cd ./ephemerol
pip install -r requirements.txt
py.test
```

## Deploy to Cloud Foundry
```
cd ./ephemerol
mkdir ./vendor
pip install --no-use-wheel --download vendor -r requirements.txt
cf push ephemerol -b python_buildpack -m 1G
```
