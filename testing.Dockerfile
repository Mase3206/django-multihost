FROM rockylinux:9

RUN dnf install -y git make vim ncurses python3.12 python3.12-pip jq sudo
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 20
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 20
RUN python -m pip install pyyaml

RUN dnf install -y dnf-plugins-core && \
	dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

RUN dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# RUN systemctl enable --now docker

RUN mkdir /django

WORKDIR /django/source
CMD cp -r /django/source-ro/* /django/source/ && bash