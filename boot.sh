#!/bin/sh
# this script is used to boot a Docker container
echo "where is this running?"
echo $(pwd)
echo $(ls)
. venv/bin/activate
export MONGO_USER="armand-admin"
export MONGO_PASSWORD="M2hZcEWo8ApIerOF"
#exec bash
#exec gunicorn -b :${PORT} dota_toolbox
#. env.sh
exec gunicorn dota_toolbox:app