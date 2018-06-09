#!/bin/sh

coverage run --branch --omit=test*,svd/__init__.py test.py
coverage html
