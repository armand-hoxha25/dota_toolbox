#!/bin/sh
# this script is used to boot a Docker container
echo "where is this running?"
echo $(pwd)
echo $(ls)
. venv/bin/activate

#exec bash
#exec gunicorn -b :${PORT} dota_toolbox
exec gunicorn dota_toolbox:app