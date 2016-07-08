# ephemerol
A Cloud Native readiness scanner that has configurable rules for Java, .NET and other cloud native application types.
[![Build Status](https://travis-ci.org/Pivotal-Field-Engineering/ephemerol.png?branch=master)](https://travis-ci.org/Pivotal-Field-Engineering/ephemerol)

Currently, ephemerol scans project source files in a zip file for the following languages:
* [Java](docs/Java.MD)
* [.NET Framework (not .NET Core)](docs/DotNet.MD)

## Requirements
Python 2.7.9

## Development
### Run Web Application Locally
Run the script as follows to get information on how to invoke it:
```
pip install -r requirements.txt
python ./ephemerol/ephemerol-web.py
```

### Testing
To run tests, make sure to install dependencies, then you can run all the tests with the `py.test` command at the root of the project.
```
pip install -r requirements.txt
py.test
```

## Deploy to Cloud Foundry
```
mkdir ./vendor
pip install --no-use-wheel --download vendor -r requirements.txt
cf push
```

The push process will take a while because we're using pandas and numpy.  Go grab a coffee and you should come back to a running ephemerol.
