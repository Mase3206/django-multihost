USER := $(shell id -un)
CWD := $(shell pwd)

help:
	echo "User: $(USER)"
	echo "CWD: $(CWD)"

groups: 
	sudo usermod -a -G docker $(USER)
	sudo groupadd classadmin
	sudo usermod -a -G classadmin $(USER)
	@echo "You'll need to restart for the group changes to take effect."

install:
# sudo dnf install -y python3.12 python3.12-pip jq
# sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.12 20
# python -m pip install pyyaml
# sudo docker run hello-world > /dev/null &2>1

	sudo chown -R $(USER):classadmin ./*
	sudo chmod -R 664 ./*
	sudo chmod 775 ./deploy.py
	sudo chmod 774 ./create-group.sh
# groups should not have execute access to create more groups

	sudo ln -s /django/source/deploy.py /usr/local/bin/deploy
#	sudo chown $(USER):classadmin /usr/local/bin/deploy

	sudo ln -s /django/source/create-group.sh /usr/local/bin/create-group
#	sudo chown $(USER):classadmin /usr/local/bin/create-group

remove:
	sudo rm /usr/local/bin/create-group
	sudo rm /usr/local/bin/deploy
