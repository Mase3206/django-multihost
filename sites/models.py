from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


from deploy.models import Deployment

# Create your models here.
class Site(models.Model):
	name = models.CharField(max_length=30, blank=False, null=False)
	deployment = models.OneToOneField(
		Deployment, 
		on_delete=models.SET_NULL,
		related_name='site',
		blank=True,
		null=True
	)
	
	description_brief = models.TextField('brief description', max_length=500, blank=False, null=True)
	description = models.TextField(blank=False, null=False)

	def __str__(self) -> str:
		return f'{self.name}'
	

@receiver(post_delete, sender=Site)
def delete_orphaned_deployment(sender, instance, **kwargs):
	if instance.deployment:
		instance.deployment.delete()