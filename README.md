AKIndices --- Alaska climate data
=================================

Air temperature data from over 400 communities, reduced to relevant engineering parameters.

What is it?
-----------

[AKIndices](http://akindices.akdillon.net) is a Flask-driven web-app that builds on the AKExtract project to provide an easy-to-use interface for working with SNAP datasets.

Prerequisites
-------------

- [AKExtract](http://github.com/thermokarst/akextract)
- Flask (0.10.1)
- SQLAlchemy (0.8.2)
- psycopg2 (2.5.1)
- flask-wtf (0.9.1)
- numpy (1.7.1)
- PostgreSQL


Installation
------------

1) Clone the repo:

    git clone https://github.com/thermokarst/akindices

2) Get the data from http://snap.uaf.edu

3) Copy `config.py.default` to `config.py`, edit the parameters to suit your needs.

4) Launch a python interpreter and populate the database with data:

    $ python
    >>> import akindices
    >>> akindices.database.init_db()

5) Launch the application with:

    $ ./run.py


Contact
-------

Do you have an idea for a feature? Find a bug?
Reach me at [mrdillon@alaska.edu](mailto:mrdillon@alaska.edu)
