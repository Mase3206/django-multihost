from typing import Any

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
from deploy.helpers import random_string

from . import (
	DEPLOY_COMPOSE_ROOT,
	DEPLOY_VOL_ROOT,
)



def create(form: QuickcreateCreationMultiForm, context: dict[str, Any]):
	# create deployment object
	deployment: Deployment = form['deployment'].save()
	site = Site.objects.get(pk=context['site_pk'])
	site.deployment = deployment
	site.save()


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
