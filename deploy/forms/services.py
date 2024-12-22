from django.forms import ModelForm

from deploy.models.services.sgi import (
	Gunicorn,
)
from deploy.models.services.db import (
	Postgres,
)


class GunicornQuickcreateForm(ModelForm):
	class Meta:
		model = Gunicorn
		fields = [
			'volumes',
			'networks',
			'environment',
			'labels',
			'database',
			'django_project_folder',
		]
		# these will be set programatically
		exclude = [
			'volumes',
			'networks',
			'environment',
			'labels',
			'database',
		]


class PostgresQuickcreateForm(ModelForm):
	class Meta:
		model = Postgres
		fields = [
			'volumes',
			'networks',
			'environment',
			'labels',
			'name', 
			'username',
			'password',
		]
		# all fields will be set programatically
		exclude = fields
