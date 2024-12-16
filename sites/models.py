from django.db import models

# Create your models here.
class Site(models.Model):
	name = models.CharField(max_length=30, blank=False, null=False)
	path = models.CharField(max_length=30, blank=False, null=False)
	
	remote_repo = models.URLField(blank=False, null=False)
	description_brief = models.TextField('brief description', max_length=500, blank=False, null=True)
	description = models.TextField(blank=False, null=False)
	use_bundled_db = models.BooleanField(blank=False)

	def __str__(self) -> str:
		return f'{self.name}'
	
