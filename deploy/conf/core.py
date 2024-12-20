from __future__ import annotations

from deploy import exceptions

from deploy.conf.service import (
	ServiceConf,
	S
)





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

	def getRootDictConfs(self):
		"""
		Return the root-level dicts (or YAML or JSON) for volumes and networks.
		"""
		nets: list[dict] = []
		vols: list[dict] = []

		for s in self.services:
			for n in s.networks:
				# deduplicate, as networks can be shared
				if n not in nets:
					nets.append(n.rootConf)
			
			for v in s.volumes:
				# we only care about non-folder mounts
				if v.typ != 'folder':
					# this will never be none if this check passes
					vols.append(v.rootConf) #type:ignore

		return {
			'volumes': {v['name']: v for v in vols},
			'networks': {n['name']: n for n in nets},
		}
	

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
