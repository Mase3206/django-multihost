from django.contrib import admin

from .models import (
	Gunicorn,
	Postgres,
	Volume,
	Network,
	EnvironmentVariable,
	Label,
	Deployment
)
import re




# Register your models here.
@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
	fields = []
	list_display = [
		'__str__',
		'git_repo',
		'online',
		'modified'
	]

@admin.register(Gunicorn)
class GunicornAdmin(admin.ModelAdmin):
	fields = []
	list_display = [
		'__str__',
		'deployment',
		'database',
		# 'online',
		# 'modified'
	]

@admin.register(Postgres)
class PostgresAdmin(admin.ModelAdmin):
	fields = []
	list_display = [
		'__str__',
	]

@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
	fields = []
	list_display = [
		'host_path_formatted',
		'guest_path'
	]

	@admin.display(description="Host path")
	def host_path_formatted(self, obj):
		split: list[str] = obj.host_path.split('/')
		return '/'.join(split[-4:])
	

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
	fields = []
	list_display = [
		'name',
		'external',
	]


@admin.register(EnvironmentVariable)
class EnvironmentVariableAdmin(admin.ModelAdmin):
	fields = []
	list_display = [
		'name',
		'redact_value_if_secret',
	]


	@admin.display(description="Value")
	def redact_value_if_secret(self, obj):
		catch = [
			r'secret',
			r'pass(?:w(?:or)d)',
		]
		if any(map(lambda v: re.findall(v, obj.name, re.IGNORECASE), catch)):
			return '<hidden>'
		else:
			return f'{obj.value}'
		

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
	fields = []
	list_display = [
		'name',
		'value'
	]
