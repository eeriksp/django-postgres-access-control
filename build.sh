#!/usr/bin/env bash

set -eu

# Run the tests
# ./test.sh

# Remove old builds
rm dist -r || true

# Build
python3.8 -m build

