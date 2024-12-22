from typing import Any
from pathlib import Path
from django.db import models

from django.conf import settings
"""
- DEPLOY_GIT_ROOT
- DEPLOY_VOL_ROOT
- DEPLOY_COMPOSE_ROOT
"""

DEPLOY_GIT_ROOT = Path(settings.DEPLOY_GIT_ROOT)
DEPLOY_VOL_ROOT = Path(settings.DEPLOY_VOL_ROOT)
DEPLOY_COMPOSE_ROOT = Path(settings.DEPLOY_COMPOSE_ROOT)

import subprocess
import json

from .services import Gunicorn
from .services import Postgres



class Deployment(models.Model):
	"""
	A pseudo-abstraction of Docker Compose.
	"""
	pk: int

	git_repo = models.URLField()
	online = models.BooleanField(default=False, null=True)
	modified = models.BooleanField(
		default=False,
		null=True,
		help_text="Deployment settings have been modified, but the deployed Docker Compose stack has not been restarted."
	)

	@property
	def git_folder(self):
		return DEPLOY_GIT_ROOT / str(self.pk)

	@property
	def volumes_folder(self):
		return DEPLOY_VOL_ROOT / str(self.pk)

	@property
	def compose_file(self):
		return DEPLOY_COMPOSE_ROOT / str(f'{self.pk}.yml')

	sgi_server = models.OneToOneField(
		Gunicorn,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	database = models.OneToOneField(
		Postgres,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)


	def _run_compose_command(self, subcommand: str, args: list[str]=[]):
		"""
		Interact with the Docker daemon via Docker Compose and subprocess. The docker-compose.yml file stored in this model is used.

		Arguments
		---------
			subcommand (str) : docker compose subcommand to run
			args (list[str]) : list of arguments to pass to the subcommand

		Returns
		-------
			CompletedProcess
		"""
		cmd = [
			'docker', 'compose', 
			'-f', f'{self.compose_file:s}',
			subcommand, *args
		]
		return subprocess.run(
			cmd, 
			stdout=subprocess.PIPE, 
			stderr=subprocess.PIPE, 
			encoding='UTF-8'
		)

	def up(self):
		return self._run_compose_command('up', args=['-d'])
	
	def down(self):
		return self._run_compose_command('down')
	
	def ps(self) -> dict[Any, Any]:
		out = self._run_compose_command('ps', args=['--format', 'json'])
		return json.loads(out.stdout)


	def delete(self, *args, **kwargs):
		self.down()


		super().delete(*args, **kwargs)


	# def __str__(self):
		# return f'Deployment for {self.site}'
		# pass
