#!/bin/bash/
pytest -v
export FLASK_APP=run.py
export FLASK_ENV=development
flask run
