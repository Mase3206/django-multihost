from typing import Any
from pathlib import Path
from django.db import models

from django.conf import settings
"""
- DEPLOY_VOL_ROOT
- DEPLOY_COMPOSE_ROOT
"""

DEPLOY_VOL_ROOT = Path(settings.DEPLOY_VOL_ROOT)
DEPLOY_COMPOSE_ROOT = Path(settings.DEPLOY_COMPOSE_ROOT)

import subprocess
import json

from .services import Gunicorn
from .services import Postgres

from django.db.models.signals import pre_delete
from deploy.models.deletion import full_delete_deployment



class Deployment(models.Model):
	"""
	A pseudo-abstraction of Docker Compose.
	"""
	pk: int

	git_repo = models.URLField()
	modified = models.BooleanField(
		default=False,
		null=True,
		help_text="Deployment settings have been modified, but the deployed Docker Compose stack has not been restarted."
	)

	@property
	def online(self) -> bool:
		"""
		Some services are online.
		"""
		# raise NotImplementedError('Programatic online checks are still being developed.')
		return False


	@property
	def healthy(self) -> bool:
		"""
		All services are online.
		"""
		raise NotImplementedError('Programatic health checks are still being developed.')
	

	@property
	def volumes_folder(self):
		return DEPLOY_VOL_ROOT / str(self.pk)

	@property
	def compose_file(self):
		return DEPLOY_COMPOSE_ROOT / str(f'{self.pk}.yml')

	sgi_server = models.OneToOneField(
		Gunicorn,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		verbose_name="SGI server"
	)
	database = models.OneToOneField(
		Postgres,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
	)


	def _run_compose_command(self, subcommand: str, args: list[str]=[], dry_run=False):
		"""
		Interact with the Docker daemon via Docker Compose and subprocess. The docker-compose.yml file stored in this model is used.

		Arguments
		---------
			subcommand (str) : docker compose subcommand to run
			args (list[str]) : list of arguments to pass to the subcommand
			dry_run (bool = False) : print and echo command to be run

		Returns
		-------
			CompletedProcess
		"""
		cmd = [
			'docker', 'compose', 
			'-f', f'{self.compose_file}',
			subcommand, *args
		]
		if dry_run:
			out = subprocess.run(
				['echo', *cmd],
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE, 
				encoding='UTF-8'
			)
			print(out.stdout)
			return out
		else:
			return subprocess.run(
				cmd, 
				stdout=subprocess.PIPE, 
				stderr=subprocess.PIPE, 
				encoding='UTF-8'
			)


	def up(self):
		return self._run_compose_command('up', args=['-d'], dry_run=True)
	
	def down(self):
		return self._run_compose_command('down', dry_run=True)
	
	def restart(self):
		return self._run_compose_command('restart', args=['-d'], dry_run=True)
	
	# TODO
	def update(self): pass
		

	def ps(self) -> dict[Any, Any]:
		out = self._run_compose_command('ps', args=['--format', 'json'])
		return json.loads(out.stdout)
	


	def __str__(self):
		if self.site:  # reverse oto association #type:ignore
			return f'Deployment for "{self.site}"' #type:ignore
		else:
			return f'Deployment object {self.pk} (unlinked)'


pre_delete.connect(full_delete_deployment, sender=Deployment)
