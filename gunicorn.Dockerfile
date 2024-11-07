FROM python:3.12.7-slim-bookworm

RUN apt-get update && apt-get upgrade -y && \
	apt-get install -y git curl

RUN mkdir /sites
WORKDIR /run/www/django

RUN pip install gunicorn psycopg[binary] whitenoise

# ENV PGSYSCONFDIR=/var/run/www/djsite
# ENV DJANGO_GUNICORN=true

EXPOSE 8000

# CMD gunicorn $SITE_NAME.wsgi
CMD cp -r /sites/django /run/www/ && \
	pip install --root-user-action ignore -r ./requirements.txt && \
	./manage.py migrate && \
	gunicorn --env DJANGO_SETTINGS_MODULE=$SITE_FOLDER.settings -b 0.0.0.0:8000 $SITE_FOLDER.wsgi
