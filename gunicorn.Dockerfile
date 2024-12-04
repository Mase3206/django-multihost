FROM python:3.12.7-slim-bookworm

RUN apt-get update && apt-get upgrade -y && \
	apt-get install -y git curl

RUN mkdir /sites
WORKDIR /run/www/django

RUN pip install whitenoise~=6.8 packaging~=24.2 gunicorn~=23.0 psycopg~=3.2 "psycopg[binary]~=3.2" environs~=11.2

# ENV PGSYSCONFDIR=/var/run/www/djsite
# ENV DJANGO_GUNICORN=true

EXPOSE 8000


CMD cp -r /sites/django /run/www/ && \
	pip install --upgrade --root-user-action ignore -r ./requirements.txt && \
	python manage.py migrate && \
	python manage.py collectstatic --noinput && \
	gunicorn --env DJANGO_SETTINGS_MODULE=$SITE_FOLDER.settings -b 0.0.0.0:8000 $SITE_FOLDER.wsgi
