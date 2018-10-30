# PyBagIt v1.5

[![Build Status](https://travis-ci.com/deepio/pybagit.svg?branch=master)](https://travis-ci.com/deepio/pybagit)

This module helps with creating an managing BagIt-compliant packages. It has
been created to conform to BagIt v0.97.

Documentation is available at http://ahankinson.github.io/pybagit.
Code hosting is available on GitHub at http://github.com/ahankinson/pybagit/.

## Requirements
Tested with Python 3.6
No external modules required.
Module has not been tested on Windows.


## Running Tests
There are a number of unit tests written to verify that this module functions
as expected. To run this, simply type

`python setup.py test`

in the package directory. NOTE: You will need a network connection to verify
the 'fetch' tests. If you don't have a network connection you can skip these
tests by commenting them out in 'bagtest.py'


## Setup and Install
To install this module, simply run:

`python setup.py install` (you may need to run this as a privileged user, e.g. 'sudo')
