#!/usr/bin/env bash

set -e

init_check_file='/var/run/dmh-site/.initialized'

function first_run () {
	touch $init_check_file

	if ! [ -z "$DJANGO_SUPERUSER_USERNAME" ] && \
		! [ -z "$DJANGO_SUPERUSER_EMAIL" ] && \
		! [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
		cat <<-EOF
			Creating superuser with:
			username : $DJANGO_SUPERUSER_USERNAME
			email    : $DJANGO_SUPERUSER_EMAIL
			password : <hidden>
		EOF
		poetry run python manage.py createsuperuser --noinput
	else
		echo "Superuser information (some or all of the required: username, email, and password) was not given  via environment variables. A superuser will need to be created manually."
	fi

	DJANGO_SUPERUSER_USERNAME='admin' DJANGO_SUPERUSER_EMAIL='admin@localhost' DJANGO_SUPERUSER_PASSWORD='password' poetry run python manage.py createsuperuser --noinput

	poetry add gunicorn
}

function check_first_run () {
	[ -f "$init_check_file" ]
}


function init () {
	git clone $GIT_REPO ./site
	mv ./site/* ./
	rm -rf ./site

	poetry install
	poetry run python manage.py migrate
	poetry run python manage.py collectstatic --noinput
}

function start () {
	poetry run gunicorn -b 0.0.0.0:8000 $PROJECT_FOLDER.wsgi
}


# check if this volume has been initalized
# if not, initialize it

init

check_first_run || first_run


start