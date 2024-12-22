Docs: https://docker-py.readthedocs.io/en/stable/containers.html

- image *(str)* = ServiceConf.image
- detach *(bool)* = (lit.) True
	- returns a [`Container` object](https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.Container)
- environment *(dict or list)* = ServiceConf.environment
	- I'll need to convert the list\[EnvironmentVariable] type to a dict.
- labels *(dict or list)* = ServiceConf.labels
	- need to convert to dict
- mounts *(list\[docker.types.Mount])* = ServiceConf.volumes
	- need to convert each object from deploy.conf.service.parts.Volume to docker.types.Mount
- name *(str)* = ServiceConf.name
- network *(str)* = ServiceConf.networks[0]
	- need to convert deploy.conf.service.parts.Network to str
	- additional networks must be added after the fact with docker.types.Network.connect()
- ports *(dict)*
	- Ports to bind inside the container.
	- The keys of the dictionary are the ports to bind inside the container, either as an integer or a string in the form port/protocol, where the protocol is either tcp, udp, or sctp.
	- The values of the dictionary are the corresponding ports to open on the host, which can be either:
		- The port number, as an integer. For example, {'2222/tcp': 3333} will expose port 2222 inside the container as port 3333 on the host.
		- None, to assign a random host port. For example, {'2222/tcp': None}.
		- A tuple of (address, port) if you want to specify the host interface. For example, {'1111/tcp': ('127.0.0.1', 1111)}.
		- A list of integers, if you want to bind multiple host ports to a single container port. For example, {'1111/tcp': [1234, 4567]}.