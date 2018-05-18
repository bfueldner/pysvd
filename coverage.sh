#!/bin/sh

coverage run --omit=test*,svd/__init__.py test.py
coverage html
