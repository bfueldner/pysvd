[![PyPI](https://img.shields.io/pypi/v/pysvd.svg)](https://pypi.org/project/pysvd)
[![PyPI - Python versions](https://img.shields.io/pypi/pyversions/pysvd.svg)](https://pypi.org/project/pysvd)
[![PyPI - License](https://img.shields.io/pypi/l/pysvd.svg)](https://pypi.org/project/pysvd)
[![Travis (.org)](https://img.shields.io/travis/bfueldner/pysvd.svg)](https://travis-ci.org/bfueldner/pysvd)
[![Coveralls github](https://img.shields.io/coveralls/github/bfueldner/pysvd.svg)](https://coveralls.io/github/bfueldner/pysvd)

# pysvd

Python System View Description format parser.

## Conformance

This parser is build to reflect 1:1 the XSD format behind SVD. The only compromis has been made by the nodes 'peripherals', 'registers' and 'fields' that are simple list of the equivalent objects.

The node names and attributes follow the same naming convention in XML as in Python to map them easier between the models.
