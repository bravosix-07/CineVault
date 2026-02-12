#!/bin/sh
# Entrypoint to run the Flask app with gunicorn
exec gunicorn --bind 0.0.0.0:5000 app:app