#!/usr/bin/env bash
set -o errexit

# Install the Python packages
pip install -r requirements.txt

# Collect static files for production
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate