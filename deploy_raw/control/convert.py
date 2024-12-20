"""
Not sure if this will be used
"""

from deploy_raw import exceptions

from deploy_raw.conf import StackConf
from deploy_raw.conf.service import ServiceConf
from deploy_raw.conf.service.parts import (
	Volume
)


import docker
from docker.types import (
	Mount, 
	DriverConfig,
)

client = docker.from_env()



def _volumeType(orig: Volume):
	if type(orig) == Volume:
		match orig.typ:
			case 'folder': return 'bind'
			case 'docker': return 'volume'
			case _: return ''
	else:
		raise TypeError('Can only convert from our Volume type.')



def toContainer(service: ServiceConf):
	mounts: list[Mount] = []
	for vol in service.volumes:
		mounts.append(Mount(
			target=str(vol.guest),
			source=str(vol.host),
			type=_volumeType(vol),
			labels={vol.name: vol.name} if vol.typ == 'docker' else None,
			driver_config=DriverConfig(vol.name, vol.rootConf[vol.name]) if vol.typ == 'docker' else None, #type:ignore
		))


	container = client.containers.create(
		service.image, 
		detach=True,
		environment=service.envToDict(),
		labels=service.labelsToDict(),
		mounts=mounts,
		name=service.name,
		network=service.networks[0].name, # primary
	)

