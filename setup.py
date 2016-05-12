from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
import io
import os
import sys

import ephemerol

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename) as f:
            buf.append(f.read())
    return sep.join(buf)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='ephemerol',
    version=ephemerol.__version__,
    url='https://github.com/Pivotal-Field-Engineering/ephemerol',
    license='None',
    author='Chris DeLashmutt',
    tests_require=['pytest', 'mock'],
    install_requires=['terminaltables'],
    cmdclass={'test': PyTest},
    author_email='cdelashmutt@pivotal.io',
    description='A Cloud Native readiness scanner',
    packages=['ephemerol'],
    include_package_data=True,
    platforms='any',
    extras_require={
        'testing': ['pytest'],
    }
)
