pysvd
=====

.. image:: https://img.shields.io/pypi/v/pysvd.svg
    :target: https://pypi.org/project/pysvd
    :alt: Latest version on pypi

.. image:: https://img.shields.io/pypi/pyversions/pysvd.svg
    :target: https://pypi.org/project/pysvd
    :alt: Python versions

.. image:: https://img.shields.io/pypi/l/pysvd
    :target: https://pypi.org/project/pysvd
    :alt: PyPI - License

.. image:: https://travis-ci.org/bfueldner/pysvd.svg?branch=master
    :target: https://travis-ci.org/bfueldner/pysvd

.. image:: https://coveralls.io/repos/github/bfueldner/pysvd/badge.svg?branch=master
    :target: https://coveralls.io/github/bfueldner/pysvd?branch=master

A **S**\ ystem **V**\ iew **D**\ escription parser package for python.

This library supports Python 3.4+.


Installation
------------

Install from PyPI_ using pip::

    $ pip install pysvd

Install from latest master on GitHub::

    $ pip install https://github.com/bfueldner/pysvd/archive/master.zip

If you want to be able to change the code while using it, clone it and install the required pip packages::

    $ git clone https://github.com/bfueldner/pysvd.git
    $ cd pysvd
    $ pip install -e .

Conformance
-----------

This parser is build to reflect 1:1 the XSD format behind SVD. The only compromis has been made by the nodes 'peripherals', 'registers' and 'fields' that are simple list of the equivalent objects.

The node names and attributes follow the same naming convention in XML as in Python to map them easier between the models.

.. _PyPi: https://pypi.org
