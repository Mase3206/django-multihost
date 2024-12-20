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