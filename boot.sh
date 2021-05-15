#!/bin/sh
# this script is used to boot a Docker container
source venv/bin/activate

exec gunicorn -b :5000  dota_toolbox:app