from django.contrib import admin

from .models import (
	Gunicorn,
	Postgres,
	Volume,
	Network,
	EnvironmentVariable,
	Label,
)

# Register your models here.
@admin.register(Gunicorn)
class GunicornAdmin(admin.ModelAdmin):
	pass

@admin.register(Postgres)
class PostgresAdmin(admin.ModelAdmin):
	pass

@admin.register(Volume)
class VolumeAdmin(admin.ModelAdmin):
	pass

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
	pass

@admin.register(EnvironmentVariable)
class EnvironmentVariableAdmin(admin.ModelAdmin):
	pass

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
	pass
