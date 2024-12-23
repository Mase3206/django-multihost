#!/usr/bin/env bash

init_check_file='/var/dmh/.initialized'

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
		poetry run manage createsuperuser --noinput
	else
		echo "Superuser information (some or all of the required: username, email, and password) was not given  via environment variables. A superuser will need to be created manually."
	fi

	DJANGO_SUPERUSER_USERNAME='admin' DJANGO_SUPERUSER_EMAIL='admin@localhost' DJANGO_SUPERUSER_PASSWORD='password' poetry run manage createsuperuser --noinput
}

function check_first_run () {
	[ -f "$init_check_file" ]
}


function init () {
	poetry install
	poetry run manage migrate
	poetry run manage collectstatic --noinput
}

function start () {
	poetry run gunicorn -b 0.0.0.0:8000 django_multihost.wsgi
}


# check if this volume has been initalized
# if not, initialize it

init

check_first_run || first_run


start