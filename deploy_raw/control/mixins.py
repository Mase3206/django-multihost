"""Docker API interface."""

import docker
from deploy_raw import exceptions

client = docker.from_env()



class DockerBuildMixin:
	buildProgress = 'rawjson'

	def __init__(self, dockerfile='', tag='', context='.') -> None:
		required = ['dockerfile', 'tag', 'context']
		missing = []

		for v in required:
			try:
				setattr(self, v, locals()[v])
			except KeyError:
				missing.append(v)

		if len(missing) > 0:
			raise exceptions.MixinMissingAttributesError(f'DockerBuildMixin requires the following missing arguments: {missing}. Consider defining them as class constants in your subclass.')


	def build(self): ...