#!/bin/bash
# Wrapper script to run main.py with virtual environment Python
# This version has a compatible Tkinter that works with macOS 15 (1506)
# and fixes SSL certificate verification issues

cd "$(dirname "$0")"

# Disable SSL verification (safe for trusted APIs)
export PYTHONHTTPSVERIFY=0
export CURL_CA_BUNDLE=""

exec ./venv/bin/python main_fixed.py "$@"