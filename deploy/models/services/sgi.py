from django.db import models
from . import Service
from .db import Postgres


class Gunicorn(Service):
	django_project_folder = models.CharField(
		max_length=30, 
		blank=False,
		help_text='Main project folder containing the settings.py file; Ex: django_project, dj, project, etc.'
	)
	database = models.OneToOneField(
		Postgres,
		on_delete=models.DO_NOTHING  # this is only used for sharing the environment variables between the two, such as for db creds
	)