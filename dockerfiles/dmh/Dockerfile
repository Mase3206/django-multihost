FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y git python3-poetry curl iputils-ping

RUN mkdir /opt/dmh
WORKDIR /opt/dmh
VOLUME /var/dmh

ENV DJANGO_DATABASE='prod-sqlite3'

EXPOSE 8000


ADD ["account", "/opt/dmh/account"]
ADD ["deploy", "/opt/dmh/deploy"]
ADD ["django_multihost", "/opt/dmh/django_multihost"]
ADD ["sites", "/opt/dmh/sites"]
ADD ["static", "/opt/dmh/static"]
ADD ["templates", "/opt/dmh/templates"]
ADD ["LICENSE", "/opt/dmh"]
ADD ["manage.py", "/opt/dmh"]
ADD ["package-lock.json", "/opt/dmh"]
ADD ["package.json", "/opt/dmh"]
ADD ["poetry.lock", "/opt/dmh"]
ADD ["pyproject.toml", "/opt/dmh"]
ADD ["README.md", "/opt/dmh"]

ADD ["dockerfiles/dmh/entrypoint.sh", "/opt/dmh"]

CMD ./entrypoint.sh
# CMD bash
