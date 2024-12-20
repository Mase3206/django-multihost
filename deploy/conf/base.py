from __future__ import annotations
from typing import Type, TypeVar

import random, string
from pathlib import Path, PosixPath
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
	upper = list(string.ascii_uppercase)
	lower = list(string.ascii_lowercase)
	numbers = list(range(0, 10))
	chars = upper + lower + numbers
	toJoin = [str(chars[random.randint(0, len(chars)-1)]) for _ in range(len(chars))]
	return ''.join(toJoin)



class StackConf:
	def __init__(self, stackName: str) -> None:
		self.name = stackName
		# this complains about this type annotation having "no meaning in the 
		# given context", but it's fine to ignore
		self.services: list[S] = []  # type: ignore[no-untyped-def]

	def get(self, service: str):
		for s in self.services:
			if s.name == service:
				return s

	def append(self, service: ServiceConf):
		self.services.append(service)

	def pop(self, service: str | ServiceConf):
		"""
		Remove the given service (by name or reference) and return it.
		"""
		if type(service) == ServiceConf:
			self.services.remove(service)
			return service
		elif type(service) == str:
			found = self.get(service)
			if not found:
				raise exceptions.ServiceNotFoundError(f'Given service name {service} not found.')
			self.services.remove(found)
			return found
		else:
			raise TypeError('"service" argument must be of type str or ServiceConf.')
		
	def remove(self, service: str | ServiceConf):
		"""
		Remove the given service (by name or reference).
		"""
		# run pop but don't return the popped service
		self.pop(service)

	

	# metaclasses
	def __str__(self) -> str:
		return f'{self.name}'
	
	# get list index
	def __getitem__(self, index: int) -> ServiceConf:
		return self.services[index]
	
	# len() of self.services
	def __len__(self) -> int:
		return len(self.services)
	
	# +=
	def __iadd__(self, services: list[S]):
		for s in services:
			self.append(s)
		return self
	
	def __repr__(self) -> str:
		return f"StackConf(name='{self.name}', services={self.services})"
	


class ServiceConf:
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

	
	def _addParts(self): ...

	def __repr__(self) -> str:
		vs: list[str] = []
		for k, v in self.__dict__.items():
			if type(v) == str:
				vs.append(f"{k}='{v}'")
			else:
				vs.append(f'{k}={v}')

		n = type(self).__name__

		return f'{n}({', '.join(vs)})'


S = TypeVar('S', bound=ServiceConf)


class DBConf(ServiceConf):
	def __init__(self, serviceName='db', dbName='db', username='user', password='password', *args, **kwargs):
		super().__init__(name=serviceName, *args, **kwargs)
		self.dbName = dbName
		self.username = username
		if password == 'password':
			print('WARNING: Using the default insecure password. Please change the set password in your database configuration!')
		self.password = password


class PostgresConf(DBConf):
	def __init__(self, dbName='pgdb', username='pguser', password=randomString(32), *args, **kwargs):
		super().__init__(
			serviceName='postgres',
			dbName=dbName,
			username=username,
			password=password,
			*args, **kwargs
		)
		self._addParts()


	def _addParts(self):
		self.volumes += [
			Volume('./.volumes/db', '/var/lib/postgresql/data')
		]
		self.environment += [
			EnvironmentVariable('POSTGRES_DB', self.dbName),
			EnvironmentVariable('POSTGRES_USER', self.username),
			EnvironmentVariable('POSTGRES_PASSWORD', self.password),
		]
		self.networks += [
			Network('default')
		]



class SiteConf(ServiceConf, DockerBuildMixin):
	image = 'mase3206/gunicorn'

	dockerfile = './deploy/dockerfiles/gunicorn.Dockerfile'
	tag = 'v0.2'
	context = './deploy/dockerfiles/'

	def __init__(self, groupName: str, sitePath: str, projectFolder: str, database: DBConf, secretKey='', debug=False, *args, **kwargs):
		super().__init__('gunicorn')
		self.sitePath = sitePath
		self.projectFolder = projectFolder
		self.database = database
		if secretKey == '':
			self.secretKey = randomString(40)
		else:
			self.secretKey = secretKey
		self._debug = debug

	
	@property
	def debug(self) -> int:
		return int(self.debug)



	def _getProjectFolder(self):
		raise NotImplementedError()
		# expectedProjectFolders = ['django', 'django_site', 'django_project', 'dj']
		# pfName = ''
		# found = False
		# auto = False
		# for pf in expectedProjectFolders:
		# 	found = path.isdir(thisFolder + '/site/' + pf)
		# 	if found:
		# 		auto = True
		# 		pfName = pf
		# 		break
		
		# # set manually if detection fails
		# if not found:
		# 	pfName = input('Django project folder not detected automatically in the site folder. Please enter the name of the Django project folder (ex: django_project, dj): ')
		# 	while not path.isdir(thisFolder + '/site/' + pfName):
		# 		pfName = input('Given Django project folder does not exist in the site folder. Please enter the name of the Django project folder (ex: django_project, dj): ')

		# return pfName

	
	def _addParts(self):
		self.volumes += [
			Volume('./siteroot', '/sites/django'),
			Volume('./.volumes/gunicorn', '/run/www/django'),
		]
		self.environment += [
			*self.database.environment,
			EnvironmentVariable('DJANGO_DATABASE', 'prod'),
			EnvironmentVariable('SITE_PATH', self.sitePath),
			EnvironmentVariable('PROJECT_FOLDER', self.projectFolder),
			EnvironmentVariable('SECRET_KEY', self.secretKey),
			EnvironmentVariable('DEBUG', str(self.debug)),
		]

