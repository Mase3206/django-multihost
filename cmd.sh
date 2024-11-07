#!/usr/bin/env bash





function do_traefik() {
	if [ -f docker-compose.traefik.yml ]; 
		echo "Traefik compose file not present in this directory. Groups share one Traefik instance, so this is expected."
		exit 2
	fi

	case $1 in
		start) start_traefik $@ ;;
		stop) stop_traefik $0 ;;
	esac

	docker compose -f docker-compose.traefik.yml up -d
}

function do_site() {
	if [ -f docker-compose.site.yml ];
		echo "Site docker-compose file not present in this directory. Did you initialize your group's folder correctly?"
		exit 2
	fi
	
	docker compose -f docker-compose.site.yml up -d
}


function do_start() {
	case $1 in
		traefik) start_traefik $@ ;;
		site) start_site $@
	esac
}

function start_traefik() {

}

function start_site() {
	
}



function do_help() {
	echo "./start.sh (traefik|site)"
	exit 1
}


case $1 in
	start) do_start $@ ;;
	stop) do_stop $@ ;;
	status) do_status $@ ;;
	*) do_help
esac