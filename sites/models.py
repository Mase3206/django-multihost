from django.db import models

from deploy.models import Deployment

# Create your models here.
class Site(models.Model):
	name = models.CharField(max_length=30, blank=False, null=False)
	deployment = models.OneToOneField(
		Deployment, 
		on_delete=models.CASCADE,
		related_name='site',
		blank=True,
		null=True
	)
	
	description_brief = models.TextField('brief description', max_length=500, blank=False, null=True)
	description = models.TextField(blank=False, null=False)

	def __str__(self) -> str:
		return f'{self.name}'
	
