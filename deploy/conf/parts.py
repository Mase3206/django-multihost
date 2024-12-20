from deploy import exceptions
from pathlib import Path, PosixPath



class Part:
	@property
	def full(self) -> str: ...

	def __str__(self): return self.full



class Volume(Part):
	def __init__(self, host: Path | str, guest: PosixPath | str, mode='', typ='folder', name='') -> None:
		if typ == 'folder' and type(host) == str:
			self.host = Path(host)
		else:
			self.host = host

		if type(guest) == str:
			self.guest = PosixPath(guest)
		else:
			self.guest = guest
		
		self.mode = mode
		self.typ = typ
		if self._validateName(name):
			self.name = name

	@property
	def full(self):
		a = [
			self.host,
			self.guest
		]
		if self.mode != '':
			a.append(self.mode)
		return ':'.join(a)
	
	@property
	def rootConf(self):
		if self.typ == 'docker':
			return { self.name: {} }
		

	def _validateName(self, name: str) -> bool:
		# the `name` attr is only needed for docker volume mounts
		if self.typ == 'docker':
			if name == '':
				return False
			
		return True
	


class Network(Part):
	def __init__(self, name: str, external=False):
		self.name = name
		self.external = external

	@property
	def full(self):
		return self.name
	
	@property
	def rootConf(self):
		return { self.name: {
			'name': self.name,
			'external': self.external
		}}
	


class EnvironmentVariable(Part):
	def __init__(self, name: str, value: str) -> None:
		if self._validateName(name):
			self.name = name
		else:
			raise exceptions.ValidationError('Given name contains illegal characters for environment variables. It must be uppercase, and must not contain $, #, _, or numbers.')
		
		self.value = value


	@property
	def full(self):
		return f'"{self.name}={self.value}"'


	def _validateName(self, name: str) -> bool:
		if ('-' or '$' or '#') in name.split(''):
			return False
		
		if (0 or 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8 or 9) in name.split(''):
			return False
		
		if name != name.upper():
			return False
		
		return True
	


class Port(Part):
	def __init__(self, host: int, guest: int) -> None:
		if type(host) == int:
			self.host = host
		else:
			raise TypeError('Host port must be type int.')
		
		if type(guest) == int:
			self.guest = guest
		else:
			raise TypeError('Guest port must be type int.')
		
	@property
	def full(self):
		return f'"{self.host}:{self.guest}"'



class Label(Part):
	def __init__(self, name: str, value: str):
		self.name = name
		self.value = value

	@property
	def full(self):
		return f'"{self.name}={self.value}"'
