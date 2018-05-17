#!/bin/sh

coverage run $(ls test_*.py)
coverage html
