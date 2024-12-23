#!/usr/bin/env bash

function first_run () {
	touch .initialized
}

function check_initialized () {
	[ -f ".initialized" ]
}


function pre_start () {
	poetry install
}

function start () {
	poetry run gunicorn -b 0.0.0.0:8000 django_multihost.wsgi
}


# check if this volume has been initalized
# if not, initialize it
check_initialized || first_run

pre_start
start