# dmh-site container for Poetry projects

FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y git python3-poetry curl iputils-ping

RUN mkdir /opt/dmh
WORKDIR /opt/dmh
VOLUME /var/run/dmh-site

ENV DJANGO_DATABASE='prod-dmh'

EXPOSE 8000


ADD ["dockerfiles/dmh-site/poetry/entrypoint.sh", "/opt/dmh"]

CMD ./entrypoint.sh
# CMD bash
