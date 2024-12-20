from __future__ import annotations
from typing import Type, TypeVar

import random, string
from pathlib import Path, PosixPath
from deploy import exceptions
from deploy.doma import DockerBuildMixin
from deploy.helpers import randomString
from deploy.conf.service.parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Port,
	Label,
)

from deploy.conf.service import (
	ServiceConf
)



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
