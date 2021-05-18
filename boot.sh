#!/bin/sh
# this script is used to boot a Docker container
echo "where is this running?"
echo $(pwd)
echo $(ls)
. venv/bin/activate

exec gunicorn -b :5000  app:app