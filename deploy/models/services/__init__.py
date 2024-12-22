"""
Models related to each service definition in a Docker Compose file.
"""

from __future__ import annotations
from django.db import models
from polymorphic.models import PolymorphicModel

from .parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Label,
)

from .db import Postgres
from .sgi import Gunicorn


class Service(PolymorphicModel):
	volumes = models.ManyToManyField(
		Volume,
		related_name='services'
	)
	networks = models.ManyToManyField(
		Network,
		related_name='services'
	)
	environment = models.ManyToManyField(
		EnvironmentVariable,
		related_name='services'
	)
	labels = models.ManyToManyField(
		Label,
		related_name='services'
	)


__all__ = [
	'Service',
	'Postgres',
	'Gunicorn',
]