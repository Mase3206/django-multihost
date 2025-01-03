from typing import Any
from dataclasses import dataclass

from tempfile import TemporaryDirectory
import os
from pathlib import Path
import subprocess

from sites.models import Site

from deploy.forms.quickcreate import QuickcreateCreationMultiForm
from deploy.models import Deployment
from deploy.models.services import (
	Gunicorn,
	Postgres
)
from deploy.models.services.parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Label,
)
from deploy.helpers import random_string, auto_repr
from deploy.exceptions import GitError

from . import (
	DEPLOY_COMPOSE_ROOT,
	DEPLOY_VOL_ROOT,
)

class PathResult:
	result_name = 'PathResult'

	def __init__(self, root: Path, full_path: Path, project_root: Path):
		self.root = root
		self.full_path = full_path
		self.project_root = project_root
		# grab just the parts within the project root, excluding the project root itself
		self.module_path = Path(*self.full_path.parts[len(self.project_root.parts):])

	def modulify(self) -> str:
		"""
		The settings path as a dot-separated module path for Python imports.
		"""
		parts = [*self.module_path.parts]

		# remove .py extension
		if (s := parts[-1].split('.'))[-1] == 'py':
			parts[-1] = s[0] 

		return '.'.join(parts)
	
	def __repr__(self) -> str:
		return auto_repr(self, self.result_name)


class SettingsModule(PathResult):
	root: Path
	"""The parent folder containging the settings module."""
	full_path: Path
	"""The full path to the settings module."""
	project_root: Path
	"""The root of the project."""
	module_path: Path
	"""The relative path to the settings module, relative to the project root."""

	result_name = 'SettingsModule'

	def __init__(self, root: Path, full_path: Path, project_root: Path):
		"""
		An object containing properties about the project's settings module.

		Arguments
		---------
			root (Path) : the parent folder containging the settings module
			full_path (Path) : the full path to the settings module
			project_root (Path) : the project root
		"""

		super().__init__(root, full_path, project_root)


class ManageFile(PathResult):
	root: Path
	"""The parent folder containging the manage.py file."""
	full_path: Path
	"""The full path to the manage.py file."""
	project_root: Path
	"""The root of the project."""
	module_path: Path
	"""The relative path to the manage.py file, relative to the project root."""

	result_name = 'ManageFile'

	def __init__(self, root: Path, full_path: Path, project_root: Path):
		"""
		An object containing properties about the project's manage.py file.

		Arguments
		---------
			root (Path) : the parent folder containging the manage.py file
			full_path (Path) : the full path to the manage.py file
			project_root (Path) : the project root
		"""
		super().__init__(root, full_path, project_root)


@dataclass
class PyProjectFile:
	root: Path
	full_path: Path
	project_root: Path

	@property
	def module_path(self):
		return Path(*self.full_path.parts[len(self.project_root.parts):])

	


def search_for_project_files(git_repo_url: str, branch: str = ''):
	"""
	Attempts to find (required): 
	- manage.py
	- the settings module (file or folder)
	
	Attempts to find (optional, but helpful):
	- pyproject.toml
	"""
	with TemporaryDirectory() as tmpdir:
		manfile = None
		setmod = None
		pyproj = None

		if branch != '':
			cmd = ['git', 'clone', '-b', branch, git_repo_url, tmpdir]
		else:
			cmd = ['git', 'clone', git_repo_url, tmpdir]
		out = subprocess.run(
			cmd, 
			stdout=subprocess.PIPE, 
			stderr=subprocess.PIPE, 
			encoding='UTF-8'
		)
		if out.returncode == 0:
			print(f'Cloned to {tmpdir}')
		else:
			raise GitError(f'The git clone failed. Reason: {out.stderr}')

		
		for root, dirs, files in os.walk(tmpdir):
			for f in files:
				if f == 'manage.py':
					manfile = ManageFile(Path(root), Path(root) / f, Path(tmpdir))
					print('Found manage.py file.')
				if f == 'settings.py':
					setmod = SettingsModule(Path(root), Path(root) / f, Path(tmpdir))
					print('Found settings module.')
				if f == 'pyproject.toml':
					pyproj = PyProjectFile(Path(root), Path(root) / f, Path(tmpdir))
					print('Found pyproject.toml file. This will prove useful later!')

			for d in dirs:
				if d == 'settings':
					if (Path(root) / d / '__init__.py').is_file():
						setmod = SettingsModule(Path(root), Path(root) / d, Path(tmpdir))
						print('Found settings module.')

			if manfile and setmod:
				break

	if not manfile:
		raise FileNotFoundError('The manage.py file was not found in the cloned git repository.')
	elif not setmod:
		raise FileNotFoundError('The settings module was not found in the cloned git repository.')
	else:
		return manfile, setmod, pyproj



def create(form: QuickcreateCreationMultiForm, context: dict[str, Any]):
	# create deployment object
	deployment: Deployment = form['deployment'].save()
	site = Site.objects.get(pk=context['site_pk'])
	site.deployment = deployment
	site.save()

	# manage_file, settings_module, pyproj_file = search_for_project_files(deployment.git_repo)

	# create shared objects
	internal_network = Network.objects.create(
		name=f'internal_{deployment.pk}',
		external=False,
	)
	external_proxy_network = Network.objects.get_or_create(
		name=f'traefik',
		external=True,
	)[0]


	def postgres():
		"""Create Postgres"""
		vols = [
			Volume.objects.create(
				host_path=str(DEPLOY_VOL_ROOT / f'{deployment.pk}' / 'postgres'),
				guest_path='/var/lib/postgresql/data',
				mode=''
			),
		]
		nets = [
			internal_network
		]
		envs = [
			EnvironmentVariable.objects.create(
				name='POSTGRES_DB',
				value='pgdb',
			),
			EnvironmentVariable.objects.create(
				name='POSTGRES_USER',
				value='pguser',
			),
			EnvironmentVariable.objects.create(
				name='POSTGRES_PASSWORD',
				value=random_string(32),
			)
		]
		labels: list[Label] = []

		postgres = Postgres.objects.create()
		postgres.volumes.add(*vols)
		postgres.environment.add(*envs)
		postgres.networks.add(*nets)
		postgres.save()

		return postgres
	

	def gunicorn(pg: Postgres):
		gunicorn: Gunicorn = form['gunicorn'].save()
		# create gunicorn
		vols = [
			Volume.objects.create(
				host_path=str(DEPLOY_VOL_ROOT / f'{deployment.pk}' / 'gunicorn'),
				guest_path='/var/run/dmh-site',
				mode=''
			),
		]

		nets = [
			internal_network,
			external_proxy_network,
		]

		SITE_PATH = f'sites/{site.pk}/view/'
		envs: list[EnvironmentVariable] = [
			EnvironmentVariable.objects.create(
				name='SITE_PATH',
				value=SITE_PATH
			),
			EnvironmentVariable.objects.create(
				name='PROJECT_FOLDER',
				value=gunicorn.django_project_folder
			),
			EnvironmentVariable.objects.create(
				name='SECRET_KEY',
				value=random_string(64)
			),
			EnvironmentVariable.objects.create(
				name='DEBUG',
				value='0'
			),
		]

		labels = [
			Label.objects.create(
				name='traefik.enable',
				value='true'
			),
			Label.objects.create(
				name=f'traefik.http.routers.gunicorn-{deployment.pk}.rule',
				value='Host(gunicorn)'
			),
			Label.objects.create(
				name=f'traefik.http.routers.gunicorn-{deployment.pk}.rule',
				value=f'PathPrefix(`/{SITE_PATH}`)'
			),
			Label.objects.create(
				name=f'traefik.http.routers.gunicorn-{deployment.pk}.middlewares',
				value=f'gunicorn-{deployment.pk}-stripprefix'
			),
			Label.objects.create(
				name=f'traefik.http.middlewares.gunicorn-{deployment.pk}-stripprefix.stripprefix.prefixes',
				value=f'/{SITE_PATH}'
			),
			Label.objects.create(
				name='traefik.docker.network',
				value=f'traefik'
			)
		]

		gunicorn.volumes.add(*vols)
		gunicorn.networks.add(*nets)
		gunicorn.environment.add(*envs)
		gunicorn.environment.add(*(pg.environment.all()))
		gunicorn.labels.add(*labels)
		gunicorn.save()

		return gunicorn
	

	pg = postgres()
	gc = gunicorn(pg)
	deployment.sgi_server = gc
	deployment.database = pg

	deployment.save()
