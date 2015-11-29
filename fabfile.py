#! /usr/bin/env python2
# -*- coding: utf-8 -*-

"""The Python CGI administration utility fabric file"""

from fabric.api import local

def git():
    """Setup Git"""

    local("git remote rm origin")
    local("git remote add origin https://korniichuk@github.com/korniichuk/pycgi.git")
    local("git remote add bitbucket https://korniichuk@bitbucket.org/korniichuk/pycgi.git")

def live():
    """Upload package to PyPI Live"""

    local("python setup.py register -r pypi")
    local("python setup.py sdist --format=zip,gztar upload -r pypi")

def test():
    """Upload package to PyPI Test"""

    local("python setup.py register -r pypitest")
    local("python setup.py sdist --format=zip,gztar upload -r pypitest")
