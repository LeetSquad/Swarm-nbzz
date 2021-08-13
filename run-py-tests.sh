#!/bin/bash

python3 -m venv venv
# shellcheck disable=SC1091
source   ./venv/bin/activate
pip3 install ".[dev]"

py.test ./tests/blockchain -s -v
py.test ./tests/core -s -v
py.test ./tests/wallet -s -v
