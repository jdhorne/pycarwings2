#!/usr/bin/env python

from setuptools import setup, find_packages
import codecs
import os
import re

NAME = 'pycarwings2'

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string")


# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

long_description = read('README.md')

# Note python2 required pycrpto instead of pycryptodome
setup(
    name=NAME,
    version=find_version(NAME, "__init__.py"),
    url='https://github.com/filcole/pycarwings2',
    author='Phil Cole',
    author_email='filcole@gmail.com',
    description='Python library for interacting with the Nissan Leaf Carwings telematics service',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache Software License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='nissan leaf carwings nissan+you',
    include_package_data=True,
    install_requires=[
        'PyYAML',
        'iso8601',
        'requests',
        'pycryptodome'],
    packages=find_packages(),
    setup_requires=('pytest-runner'),
    tests_require=['pytest', 'pytest-cov', 'pytest-flake8'],
)
