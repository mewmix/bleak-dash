FROM python:3

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            systemd \
            sudo \
            bluez \
    && rm -rf /var/lib/apt/lists/*

COPY . /home/dash
WORKDIR /home/dash

RUN pip install -r requirements.txt && \
    rm requirements.txt && \
    rm Dockerfile && \
    rm .gitattributes && \
    rm .gitignore
