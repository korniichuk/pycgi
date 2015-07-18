.. contents:: Table of contents
   :depth: 2

Portability
===========
The Python CGI administration utility tested on Ubuntu 14.04.2 LTS and Ubuntu 15.04.

Installation
============
Install the pycgi from PyPI
---------------------------
::

    $ sudo pip install pycgi

Install the pycgi from GitHub
-----------------------------
::

    $ sudo pip install git+git://github.com/korniichuk/pycgi#egg=pycgi

Upgrade the pycgi from PyPI
---------------------------
::

    $ sudo pip install -U pycgi

or::

    $ sudo pip install --upgrade pycgi

Uninstall the pycgi
-------------------
::

    $ sudo pip uninstall pycgi

Development installation
========================
::

    $ git clone git://github.com/korniichuk/pycgi.git
    $ cd pycgi
    $ sudo pip install .

User guide
==========
Help
----
The standard output for –help::

    $ pycgi -h

or::

    $ pycgi --help

For information on using subcommand "SUBCOMMAND", do::

    $ pycgi SUBCOMMAND -h

or::

    $ pycgi SUBCOMMAND --help

Example::

    $ pycgi install -h

Version
-------
The standard output for –version::

    $ pycgi -v

or::

    $ pycgi --version

Install the Python CGI
----------------------
::

    $ pycgi install
