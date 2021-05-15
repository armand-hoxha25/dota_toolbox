# Dockerfile Image Container

FROM openkbs/jdk-mvn-py3

RUN adduser -D dota_toolbox

WORKDIR /home/dota_toolbox

COPY requirements.txt requirements.txt

RUN python -m venv venv

RUN venv/bin/pip install -r requirements.txt

RUN venv/bin/pip install gunicorn

COPY app app

COPY clarity_jars config.py boot.sh ./
RUN chmod +x boot.sh

RUN chown -R dota_toolbox:dota_toolbox ./
USER dota_toolbox
EXPOSE 5000

ENTRYPOINT ["./boot.sh"]