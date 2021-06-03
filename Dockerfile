# Dockerfile Image Container

FROM openkbs/jdk-mvn-py3

RUN sudo adduser dota_toolbox

WORKDIR /home/dota_toolbox

COPY requirements.txt requirements.txt

RUN sudo python3 -m venv venv

RUN sudo venv/bin/pip install -r requirements.txt

RUN sudo venv/bin/pip install gunicorn

COPY app app

COPY config.py dota_toolbox.py boot.sh env.sh Procfile ./
RUN sudo chmod +x boot.sh

RUN sudo chown -R dota_toolbox:dota_toolbox ./
USER dota_toolbox
EXPOSE 8000

## compile the clarity jars


ENTRYPOINT ["./boot.sh"]