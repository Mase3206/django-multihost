FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y git curl iputils-ping 
RUN pip install poetry

RUN mkdir /opt/dmh
WORKDIR /opt/dmh

# ADD ["account", "/opt/dmh/account"]
# ADD ["deploy", "/opt/dmh/deploy"]
# ADD ["django_multihost", "/opt/dmh/django_multihost"]
# ADD ["sites", "/opt/dmh/sites"]
# ADD ["static", "/opt/dmh/static"]
# ADD ["templates", "/opt/dmh/templates"]
# ADD ["LICENSE", "/opt/dmh"]
# ADD ["manage.py", "/opt/dmh"]
# ADD ["pyproject.toml", "/opt/dmh"]
# ADD ["README.md", "/opt/dmh"]

ADD . .
ADD ["dockerfiles/dmh/entrypoint.sh", "/opt/dmh"]

# RUN poetry bundle venv --python=/usr/bin/python3 --only=main /opt/dmh/venv

RUN poetry install --only=main
# RUN poetry run manage migrate
RUN poetry run manage collectstatic --noinput


ENV DJANGO_DATABASE='prod-sqlite3'
VOLUME /var/dmh
EXPOSE 8000

ENTRYPOINT ./entrypoint.sh
