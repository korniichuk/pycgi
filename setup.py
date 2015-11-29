# -*- coding: utf-8 -*-

from os.path import dirname, join
from setuptools import setup

setup(
    author = "Ruslan Korniichuk",
    author_email = "ruslan.korniichuk@gmail.com",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities"
    ],
    description = ("The Python CGI administration utility"),
    download_url = "https://github.com/korniichuk/pycgi/archive/0.1.zip",
    entry_points = {
        'console_scripts': 'pycgi = pycgi.pycgi:main'
    },
    include_package_data = True,
    install_requires = [
        "configobj",
        "fabric"
    ],
    keywords = ["cgi", "cgi installer", "pycgi", "python cgi", "python2"],
    license = "Public Domain",
    long_description = open(join(dirname(__file__), "README.rst")).read(),
    name = "pycgi",
    packages = ["pycgi"],
    platforms = ["Linux"],
    url = "https://github.com/korniichuk/pycgi",
    version = "0.1a3",
    zip_safe = True
)
