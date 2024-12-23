FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y git python3-poetry curl iputils-ping

RUN mkdir /opt/dmh
WORKDIR /opt/dmh

EXPOSE 8000

ADD [".", "/opt/dmh"]

CMD ./dockerfiles/dmh/entrypoint.sh
# CMD bash
