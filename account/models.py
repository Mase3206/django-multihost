from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from sites.models import Site

class CustomUser(AbstractUser):
	associated_site = models.ForeignKey(
		Site, 
		on_delete=models.CASCADE,
		blank=True,
		null=True
	)
	github_username = models.CharField(
		max_length=30,
		blank=True,
		null=True
	)
	pass
