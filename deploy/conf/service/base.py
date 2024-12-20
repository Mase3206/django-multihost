from __future__ import annotations
from typing import TypeVar

from deploy import exceptions
from deploy.conf.service.parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Port,
	Label,
)



class ServiceConf:
	def __init__(
			self, 
			name: str, 
			image: str,
			volumes: list[Volume]=[], 
			environment: list[EnvironmentVariable]=[],
			networks: list[Network]=[],
			ports: list[Port]=[],
			labels: list[Label]=[],
		) -> None:
		self.name = name
		self.image = image
		self.volumes = volumes
		self.environment = environment
		self.networks = networks
		self.labels = labels

	
	def _addParts(self): ...

	def envToDict(self):
		envs = [v.toDict() for v in self.environment]
		ret: dict[str, str] = {}
		for d in envs:
			k = list(d.keys())[0]
			v = d[k]
			ret[k] = v
		return ret
	
	def labelsToDict(self):
		labels = [v.toDict() for v in self.labels]
		ret: dict[str, str] = {}
		for d in labels:
			k = list(d.keys())[0]
			v = d[k]
			ret[k] = v
		return ret


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