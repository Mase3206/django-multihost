from django.db import models

from .parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Label,
)


class Postgres(models.Model):
	volumes = models.ManyToManyField(
		Volume,
		related_name='postgres'
	)
	networks = models.ManyToManyField(
		Network,
		related_name='postgres'
	)
	environment = models.ManyToManyField(
		EnvironmentVariable,
		related_name='postgres'
	)
	labels = models.ManyToManyField(
		Label,
		related_name='postgres'
	)

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

	class Meta:
		verbose_name_plural = 'postgres containers'