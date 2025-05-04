#!/bin/bash
# Aktywuj lokalne środowisko venv
source "$(dirname "$0")/venv/bin/activate"

PORT=/dev/cu.usbserial-0001

mpremote connect $PORT cp main.py :main.py

