"""
Parts of a Docker Compose service definition: volumes, environment variables, etc.
"""

from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
"""
- DEPLOY_GIT_ROOT
- DEPLOY_VOL_ROOT
- DEPLOY_COMPOSE_ROOT
"""


class Volume(models.Model):
	"""
	Docker Compose folder-bind-type volume mount object.
	"""
	host_path = models.FilePathField(path=settings.DEPLOY_VOL_ROOT)
	guest_path = models.CharField(max_length=50, blank=False)
	mode = models.CharField(max_length=3, choices=(
		('', 'Read/write (default)'),
		('rw', 'Read/write (explicit)'),
		('ro', 'Read-only'),
	))

	@property
	def compose(self) -> str:
		"""Return object in a Compose-compatable format."""
		if self.mode == '':
			return f'{self.host_path}:{self.guest_path}'
		else:
			return f'{self.host_path}:{self.guest_path}:{self.mode}'


class Network(models.Model):
	"""
	Docker Compose network object.
	"""
	name = models.CharField(max_length=20, blank=False)
	external = models.BooleanField(default=False)

	@property
	def compose(self) -> str:
		"""Return object in a Compose-compatable format."""
		return f'{self.name}'
	

env_var_name_validator = RegexValidator(
	r'[A-Z_]',
	'Only uppercase ASCII letters and the underscore character are permitted in environment variable names.'
)
"""Limits the characters allowed when entering env var names."""
class EnvironmentVariable(models.Model):
	"""
	Docker Compose environment variable object.
	"""
	name = models.CharField(
		max_length=50,
		blank=False,
		validators=[env_var_name_validator]
	)
	value = models.CharField(
		max_length=200, 
		blank=True, 
		help_text="This can be empty."
	)

	@property
	def compose(self) -> str:
		"""Return object in a Compose-compatable format."""
		if self.value:
			return f"{self.name}='{self.value}'"
		else:
			return f"{self.name}=''"
		

class Label(models.Model):
	"""
	Docker Compose label object.
	"""
	name = models.CharField(
		max_length=200, 
		blank=False,
		help_text='Ex: "traefik.http.routers.gunicorn.rule"'
	)
	value = models.CharField(
		max_length=200, 
		blank=False,
		help_text='Ex: "Host(gunicorn)"'
	)

	@property
	def compose(self) -> str:
		"""Return object in a Compose-compatable format."""
		return f'{self.name}={self.value}'
