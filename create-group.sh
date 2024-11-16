#!/usr/bin/env bash

set -e


if [[ "$1" == "-h" ]] || [[ "$2" == "-h" ]] || [[ "$1" == "" ]] || [[ "$2" == "" ]]; then
	echo "Error: missing arguments." 
	echo "$0 term group_name"
fi


term=$1

if [ ! -d /django/$term ]; then
	echo "The given term ($term) folder doesn't exist yet. Please create this manually."
	exit 1
fi; 


# this isn't the safest code out there, but it's probably fine.
eval "groups=($2)"

source_folder=/django/source
files_to_link=(docker-compose.site.yml instructions.md)
owner_user='trishduce'
owner_group='classadmin'



for group_name in "${groups[@]}"; do
	group_folder=/django/$term/$group_name


	if [ -d $group_folder ]; then
		echo "The $group_name group already has a group folder in /django/$term."
		exit 1
	fi

	echo "Creating folder for $group_name"
	mkdir $group_folder


	for file in "${files_to_link[@]}"; do
		echo "Linking and setting permissions on $file"
		ln -s $source_folder/$file $group_folder/$file

		sudo chown $owner_user:$owner_group $group_folder/$file
		# rwx to user and group, r-x for everyone else
		sudo chmod 775 $group_folder/$file
	done
	echo
done