#!/usr/bin/env python

from os.path import join
from setuptools import setup, find_packages

NAME = 'pycarwings2'
PACKAGE = NAME.replace('-', '_')


def get_version():
    with open(join(PACKAGE, '__init__.py')) as fileobj:
        for line in fileobj:
            if line.startswith('__version__ ='):
                return line.split('=', 1)[1].strip()[1:-1]
        else:
            raise Exception(
                '__version__ is not defined in %s.__init__' % PACKAGE)

#FIXME: python2 requires pycrpto instead of pycryptodome
setup(
    name=NAME,
    version=get_version(),
    author='haykinson',
    author_email='',
    description='Python library for interacting with the Nissan CARWINGS telematics service',
    include_package_data=True,
    install_requires=[
        'PyYAML',
        'iso8601',
        'requests',
        'pycryptodome'],
    packages=find_packages(),
    setup_requires=('pytest-runner'),
    tests_require=('pytest', 'pytest-cov', 'pytest-flake8'),
)
