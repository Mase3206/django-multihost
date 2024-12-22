from django.db import models

from . import Service


class Postgres(Service):
	name = models.CharField(
		max_length=40,
		blank=False,
		default='pgdb',
		help_text='Name of the database within Postgres'
	)
	username = models.CharField(
		max_length=30,
		blank=False,
		default='pguser',
		help_text='The database username your project will use to connect to Postgres'
	)
	password = models.CharField(
		max_length=128,
		blank=False,
		default='pgpass',
		help_text='The password of the database user. Randomly generated passwords (up to 128 chars long) are highly recommended.'
	)
