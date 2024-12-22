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
		'__str__',
	]

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
		'__str__',
	]

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
	fields = []
	list_display = [
		'__str__',
	]
