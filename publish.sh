#!/usr/bin/env bash

set -eu

./build.sh

# Upload to PyPi (will prompt for username and password)
python3.8 -m twine upload dist/*
