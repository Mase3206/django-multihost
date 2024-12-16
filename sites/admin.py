from django.contrib import admin
from .models import Site

# Register your models here.

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
	fields = [
		'name',
		'path',
		'remote_repo',
	]
	list_display = fields
