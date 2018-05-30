#!/usr/bin/python

import os
from setuptools import setup, find_packages

from djweed.version import __version__


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


META_DATA = {
    'name': 'django-weed',
    'version': __version__,
    'description': "Weed-FS integration into Django as a storage",
    'long_description': read('README.md'),
    'license': 'MIT',

    'author': "Vlad Frolov",
    'author_email': "frolvlad@gmail.com",

    'url': "https://github.com/ProstoKSI/django-weed",

    'packages': find_packages(),

    'install_requires': ('django', 'pyseaweed>=0.3.3', ),
}

if __name__ == "__main__":
    setup(**META_DATA)

