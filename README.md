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
mkdir ./ephemerol/vendor
pip install --no-use-wheel --download ./ephemerol/vendor -r requirements.txt
cf push
```

## Project Core Team
#### [Chris Delashmutt/Pivotal - Project Lead](https://github.com/cdelashmutt-pivotal)
#### [James Williams/Pivotal - Committer](https://github.com/jwilliams-pivotal)

## Project Contributors
#### [John Feminella/Pivotal](https://github.com/fj)
Early adopter. Suggested we move to open source the project.

#### Dieter Flick/Pivotal
Early adopter. Provided excellent feedback on the cloud readiness index scoring algorithm.

#### [Matt Cowger/EMC](https://github.com/mcowger)
Requested that we remove pandas to reduce dependency overhead. This was an excellent idea.

