#!/bin/sh
# this script is used to boot a Docker container
echo "where is this running?"
echo $(pwd)
echo $(ls)
. venv/bin/activate
export MONGO_USER="armand-admin"
export MONGO_PASSWORD="M2hZcEWo8ApIerOF"


git clone https://github.com/skadistats/clarity-examples.git clarity-examples
ls
cd clarity-examples
mvn -P matchend package
cd ..
cp ./clarity-examples/target/matchend.one-jar.jar app/clarity_jars

#exec bash
#exec gunicorn -b :${PORT} dota_toolbox
#. env.sh
exec gunicorn dota_toolbox:app