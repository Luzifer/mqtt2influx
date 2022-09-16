FROM python:3.10-alpine

COPY requirements.txt /src/requirements.txt
WORKDIR /src

RUN set -ex \
 && pip install -r /src/requirements.txt

VOLUME ["/config"]
ENV CONFIG_PATH=/config/config.yml

COPY . /src
CMD ["/usr/local/bin/python3", "main.py"]
