from __future__ import annotations
import random, string
from deploy import exceptions
from deploy.doma import DockerBuildMixin
from deploy.conf.parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Port,
	Label,
)



def randomString(length: int):
	upper = string.ascii_uppercase.split('')
	lower = string.ascii_lowercase.split('')
	numbers = list(range(0, 10))
	chars = upper + lower + numbers
	toJoin = [str(chars[random.randint(0, len(chars)-1)]) for _ in range(len(chars))]
	return ''.join(toJoin)


class StackConf:
	def __init__(self, stackName: str) -> None:
		self.name = stackName
		self.services: list[BaseServiceConf] = []

	def get(self, service: str):
		for s in self.services:
			if s.name == service:
				return s

	def append(self, service: BaseServiceConf):
		self.services.append(service)

	def pop(self, service: str | BaseServiceConf):
		"""
		Remove the given service (by name or reference) and return it.
		"""
		if type(service) == BaseServiceConf:
			self.services.remove(service)
			return service
		elif type(service) == str:
			found = self.get(service)
			if not found:
				raise exceptions.ServiceNotFoundError(f'Given service name {service} not found.')
			self.services.remove(found)
			return found
		else:
			raise TypeError('"service" argument must be of type str or BaseServiceConf.')
		
	def remove(self, service: str | BaseServiceConf):
		"""
		Remove the given service (by name or reference).
		"""
		# run pop but don't return the popped service
		self.pop(service)


class BaseServiceConf:
	def __init__(
			self, 
			name: str, 
			volumes: list[Volume]=[], 
			environment: list[EnvironmentVariable]=[],
			networks: list[Network]=[],
			labels: list[Label]=[],
		) -> None:
		self.name = name
		self.volumes = volumes
		self.environment = environment
		self.networks = networks
		self.labels = labels


class PostgresConf(BaseServiceConf):
	def __init__(self, dbName='pgdb', username='pguser', password=randomString(32), *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.dbName = dbName
		self.username = username
		self.password = password



class SiteConf(BaseServiceConf, DockerBuildMixin):
	image = 'mase3206/gunicorn'

	dockerfile = './deploy/dockerfiles/gunicorn.Dockerfile'
	tag = 'v0.2'
	context = './deploy/dockerfiles/'

	def __init__(self, groupName: str, sitePath: str, *args, **kwargs):
		super(SiteConf).__init__(name=groupName)
