# -*- coding: utf-8 -*-

"""setup.py: setuptools control."""

from setuptools import setup
# from setuptools import setup, find_packages

import re

_version = re.search("^__version__\s*=\s*'(.*)'",
                     open('dev_path/__init__.py').read(),
                     re.M ).group(1)

with open('README.rst', 'rb') as f:
    _long_description = f.read().decode('utf-8')

setup(
    name = 'dev_path',
    version = _version,
    description = "Move* to a specified active development path via pushd",
    author = 'Philip H. Dye',
    author_email = 'philip@phd-solutions.com',
    # url = 'http://www.phd-solutions.com/philip-d-dye',
    long_description = _long_description,
    packages = ['dev_path'],
    # packages=find_packages(exclude=['t', 'tests', 'tests.*']),
    package_data={'dev_path': ['shell/*'] },
    include_package_data=True,
    entry_points = {
        'console_scripts': [ 'dev_path = dev_path:main',
                             'dev-path = dev_path:main'
        		   ] },
)
