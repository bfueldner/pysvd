#!/bin/sh

coverage run --omit=test* test.py
coverage html
