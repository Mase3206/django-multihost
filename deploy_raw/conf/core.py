from __future__ import annotations

from deploy_raw import exceptions
import re
import yaml
from pathlib import Path

from deploy_raw.conf.service import (
	ServiceConf,
	S
)
from deploy_raw.conf.service import (
	SiteConf,
	PostgresConf,
)

from deploy_raw.control.mixins import DockerBuildMixin





class StackConf:
	def __init__(self, stackName: str) -> None:
		self.name = re.sub(r' ', r'_', stackName)
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

	def getRootDictConfs(self):
		"""
		Return the root-level dicts (or YAML or JSON) for volumes and networks.
		"""
		nets: list[dict] = []
		vols: list[dict] = []

		for s in self.services:
			for n in s.networks:
				# deduplicate, as networks can be shared
				if n.toDict() not in nets:
					nets.append(n.rootConf)
			
			for v in s.volumes:
				# we only care about non-folder mounts
				if v.typ != 'folder':
					# this will never be none if this check passes
					vols.append(v.rootConf) #type:ignore

		fnets = {}
		for n in nets:
			k = list(n.keys())[0]
			fnets[k] = list(n.values())[0]

		return {
			'volumes': {v['name']: v for v in vols},
			'networks': fnets,
		}


	# @property
	# def __dict__(self):
	# 	_services = [dict(s) for s in self.services]
	# 	ret = {
	# 		'name': self.name,
	# 		'services': _services
	# 	}
	# 	return ret

	def toDict(self):
		_services = [s.toDict() for s in self.services]
		ret = {
			'name': self.name,
			'services': _services
		}
		return ret
	
	def __iter__(self):
		self._iter_index = -1
		self._iter_items = list(self.__dict__.items())
		return self
	
	def __next__(self):
		self._iter_index += 1
		if self._iter_index >= len(self._iter_items):
			raise StopIteration
		return self._iter_items[self._iter_index]


	# special methods
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
		return f"StackConf(name='{self.name}', services={repr(self.services)})"


	@staticmethod
	def fromConf(deployConf: dict) -> StackConf:
		_stackName = deployConf['name']
		stack = StackConf(_stackName)

		# _vmountType = deployConf['options']['volume mount type']
		_siteDb = deployConf['site']['database']
		for _dbc in deployConf['databases']:
			if _dbc['name'] == _siteDb:
				if _dbc['use bundled']:
					database = PostgresConf()
				elif _dbc.get('type', None) == 'postgres':
					database = PostgresConf(
						dbName=_dbc['conf']['db name'],
						username=_dbc['conf']['username'],
						password=_dbc['conf']['password'],
					)
				else:
					Exception('unsupported db type')
		
		site = SiteConf(
			groupName=deployConf['site']['group name'],
			sitePath=deployConf['site']['site path'],
			projectFolder=deployConf['site']['project folder'],
			database=database,
		)
		stack += [site, database]
		return stack
	

	def toCompose(self):
		services = {}
		for s in self.services:
			buildConf = {}
			if isinstance(s, DockerBuildMixin):
				buildConf = {
					'dockerfile': s.dockerfile,
					'context': s.context,
				}
			
			services[s.name] = {
				'image': s.image,
				'build': buildConf if buildConf else {},
				'volumes': [vol.full for vol in s.volumes],
				'environment': [env.full for env in s.environment],
				'networks': [net.full for net in s.networks],
				'ports': [port.full for port in s.ports],
				'labels': [label.full for label in s.labels],
			}


		out = {
			'name': self.name,
			'services': services,
			**self.getRootDictConfs()
		}
		# print(out)
		return out



def initializeFromYaml(yamlFile: Path | str):
	if type(yamlFile) != Path:
		yamlFile = Path(yamlFile)

	with open(yamlFile, 'r') as f:
		out = yaml.safe_load(f)

	return StackConf.fromConf(out)
