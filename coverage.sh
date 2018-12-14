#!/bin/sh

coverage3 run --branch --omit=test*,svd/__init__.py test.py
coverage3 html
