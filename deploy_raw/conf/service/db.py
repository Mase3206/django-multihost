from __future__ import annotations

from deploy_raw import exceptions
from deploy_raw.helpers import randomString
from deploy_raw.conf.service.parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Port,
	Label,
)

from deploy_raw.conf.service import (
	ServiceConf
)



class DBConf(ServiceConf):
	def __init__(
			self, 
			image: str, 
			serviceName='db', 
			dbName='db', 
			username='user', 
			password='password', 
			*args, **kwargs
		):
		super().__init__(name=serviceName, image=image, *args, **kwargs)
		self.dbName = dbName
		self.username = username
		if password == 'password':
			print('WARNING: Using the default insecure password. Please change the set password in your database configuration!')
		self.password = password


class PostgresConf(DBConf):
	def __init__(self, dbName='pgdb', username='pguser', password=randomString(32), *args, **kwargs):
		super().__init__(
			serviceName='postgres',
			image='postgres:17.0',
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