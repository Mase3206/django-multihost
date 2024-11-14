#!/usr/bin/env bash

set -e

season=$1
group_name=$2

group_folder=/django/$season/$group_name
source_folder=/django/source

files_to_link=(docker-compose.site.yml instructions.md deploy.py)
owner_user='trishduce'
owner_group='classadmin'


if [ ! -d /django/$season ]; then
	echo "The given season ($season) folder doesn't exist yet. Please create this manually."
	exit 1
fi; if [ -d $group_folder ]; then
	echo "The $group_name group already has a group folder in /django/$season."
	exit 1
fi

echo "Creating folder for $group_name"
# mkdir $group_folder


for file in ${files_to_link[@]}; do
	echo "Linking and setting permissions on $file"
	ln -s $source_folder/$file $group_folder/$file

	sudo chown $owner_user:$owner_group $group_folder/$file
	# rwx to user and group, r-x for everyone else
	sudo chmod 775 $group_folder/$file
done
