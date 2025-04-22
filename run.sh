#!/usr/bin/env bash
export FLASK_APP=src/main/python/uk/gov/hmcts/reform/dev/Application.py
export FLASK_ENV=development
export $(grep -v '^#' .env | xargs)   # load BASIC_AUTH_USERNAME/PASSWORD
flask run --host=0.0.0.0 --port=5000
