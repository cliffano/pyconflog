#!/usr/bin/env bash
set -o nounset

cd ../
. ./.venv/bin/activate
cd examples/

python3 _conflog.py