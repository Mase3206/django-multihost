"""
Parts of a Docker Compose service definition: volumes, environment variables, etc.
"""

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings

import os
"""
- DEPLOY_VOL_ROOT
- DEPLOY_COMPOSE_ROOT
"""


def validate_and_create_path(value):
	full_path = os.path.join(settings.DEPLOY_VOL_ROOT, value)
	if not os.path.exists(full_path):
		try:
			os.makedirs(full_path)
		except OSError as e:
			raise ValidationError(f"Cannot create directory: {full_path}. Error: {e}")


class Volume(models.Model):
	"""
	Docker Compose folder-bind-type volume mount object.
	"""
	host_path = models.CharField(max_length=255, validators=[validate_and_create_path])
	guest_path = models.CharField(max_length=50, blank=False)
	mode = models.CharField(max_length=10, default='default', choices=(
		('default', 'Read/write (default)'),
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
		
	def __str__(self) -> str:
		split = self.host_path.split('/')[-2:]
		return f'Volume "{split[1]}" for Deployment {split[0]}'


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
	
	def __str__(self) -> str:
		return f'Network "{self.name}"' + (' (external)' if self.external else '')
	

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
		
	def __str__(self) -> str:
		return f'({self.pk}) {self.name}'
		

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
	
	def __str__(self) -> str:
		return f'({self.pk}) {self.compose}'
