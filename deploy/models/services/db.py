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

	def __str__(self) -> str:
		return f'Postgres container {self.pk}'

	class Meta:
		verbose_name_plural = 'postgres containers'