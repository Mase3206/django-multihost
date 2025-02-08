from typing import Any
from pathlib import Path
from django.db import models

import yaml

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
from deploy.helpers import get_initials
from deploy.models.services.parts import Network



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

	sgi_server: models.OneToOneField[Gunicorn] = models.OneToOneField( #type:ignore
		Gunicorn,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		verbose_name="SGI server"
	)
	database: models.OneToOneField[Postgres] = models.OneToOneField( #type:ignore
		Postgres,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
	)

	@property
	def compose(self) -> dict[str, Any]:
		nets: set[Network] = {
			*self.sgi_server.networks.all(),
			*self.database.networks.all()
		}
		netconf = {}
		for n in nets:
			netconf[n.name] = {
				'name': n.name,
				'external': n.external,
			}
		
		out = {
			'name': get_initials(self.site.name), #type:ignore
			'services': {
				'gunicorn': {
					'image': 'ghcr.io/mase3206/dmh-site',
					'volumes': [
						*[v.compose for v in self.sgi_server.volumes.all()],
					],
					'networks': [n.compose for n in self.sgi_server.networks.all()],
					'environment': {e.name: e.value for e in self.sgi_server.environment.all()},
					'labels': [l.compose for l in self.sgi_server.labels.all()],
				},
				'postgres': {
					'image': 'postgres:17',
					'volumes': [v.compose for v in self.database.volumes.all()],
					'networks': [n.compose for n in self.database.networks.all()],
					'environment': {e.name: e.value for e in self.sgi_server.environment.all()},
				}
			},
			'networks': netconf
		}

		return out


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
		if self._check_compose_file():
			print(f'Compose file does not exist, creating at {self.compose_file}')
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
		

	def _compose_init(self):
		with open(self.compose_file, 'w+') as f:
			yaml.safe_dump(self.compose, f)


	def _check_compose_file(self, force=False) -> bool:
		"""
		Checks if the commpose file for this deployment is already created. If so, return True. If not, create it and return False.

		Arguments
		---------
			force (bool=False) : forcibly re-create the compose file, even if it already exists.
		"""

		if self.compose_file.exists():
			if force:
				self.compose_file.unlink()
				self.compose_file.touch()
				self._compose_init()

			return True
		else:
			self.compose_file.touch(exist_ok=False)
			self._compose_init()
			return False


	def up(self) -> subprocess.CompletedProcess[str]:
		return self._run_compose_command('up', args=['-d'], dry_run=False)
	
	def down(self) -> subprocess.CompletedProcess[str]:
		return self._run_compose_command('down', dry_run=False)
	
	def restart(self) -> subprocess.CompletedProcess[str]:
		return self._run_compose_command('restart', args=['-d'], dry_run=False)
	
	# TODO
	def update(self): 
		...
		

	def ps(self) -> dict[Any, Any]:
		out = self._run_compose_command('ps', args=['--format', 'json'])
		return json.loads(out.stdout)
	


	def __str__(self):
		if self.site:  # reverse oto association #type:ignore
			return f'Deployment for "{self.site}"' #type:ignore
		else:
			return f'Deployment object {self.pk} (unlinked)'


pre_delete.connect(full_delete_deployment, sender=Deployment)
