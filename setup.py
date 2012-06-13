#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Yuji
# Last Change:  5-30-2012
#
from setuptools import setup, find_packages

version = "0.1.2"

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()
setup(
    name="django-redirector",
    version=version,
    description = "",
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "django redirect 301 textarea codemirror",
    author = "Yuji Tomita",
    author_email = "yuji@grovemade.com",
    url=r"https://github.com/yuchant/django-redirector",
    license = 'Beerware',
    packages = find_packages(),
    package_dir = {
        'django_redirector': 'django_redirector',
    },
    include_package_data = True,
    zip_safe = False,
    install_requires=['setuptools'],
)
