# Dockerfile Image Container

FROM openkbs/jdk-mvn-py3

RUN sudo adduser dota_toolbox

WORKDIR /home/dota_toolbox

COPY requirements.txt requirements.txt

RUN sudo python3 -m venv venv

RUN sudo venv/bin/pip install -r requirements.txt

RUN sudo venv/bin/pip install gunicorn

COPY app app

COPY clarity_jars config.py boot.sh ./
RUN sudo chmod +x boot.sh

RUN sudo chown -R dota_toolbox:dota_toolbox ./
USER dota_toolbox
EXPOSE 5000

ENTRYPOINT ["./boot.sh"]