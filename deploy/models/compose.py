from django.db import models
from .services import Gunicorn



class Deployment(models.Model):
	"""
	A pseudo-abstraction of Docker Compose.
	"""

	git_repo = models.URLField()
	sgi_server = models.OneToOneField(
		Gunicorn,
		on_delete=models.CASCADE
	)

