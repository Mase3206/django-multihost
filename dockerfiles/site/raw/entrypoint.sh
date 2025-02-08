#!/usr/bin/env bash

set -e

init_check_file='/var/run/dmh-site/.initialized'
venv_name='venv'


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
		python manage.py createsuperuser --noinput
	else
		echo "Superuser information (some or all of the required: username, email, and password) was not given  via environment variables. A superuser will need to be created manually."
	fi

	DJANGO_SUPERUSER_USERNAME='admin' DJANGO_SUPERUSER_EMAIL='admin@localhost' DJANGO_SUPERUSER_PASSWORD='password' python manage.py createsuperuser --noinput
}

function check_first_run () {
	[ -f "$init_check_file" ]
}


function init () {
	git clone $GIT_REPO ./site
	mv ./site/* ./
	rm -rf ./site

	python -m venv $venv_name
	source $venv_name/bin/activate
	pip install -r requirements.txt

	python -m pip install gunicorn
	python -m pip install --upgrade 'whitenoise=6.8'

	python manage.py migrate
	python manage.py collectstatic --noinput
}

function start () {
	gunicorn -b 0.0.0.0:8000 $PROJECT_FOLDER.wsgi
}


init

# check if this volume has been initalized
# if not, initialize it
check_first_run || first_run


start