from django.forms import ModelForm

from deploy.models.services.parts import (
	Volume,
	Network,
	EnvironmentVariable,
	Label,
)


class VolumeForm(ModelForm):
	class Meta:
		model = Volume
		fields = [
			'host_path',
			'guest_path',
			'mode',
		]
		# these will be set programatically
		exclude = [
			'host_path',
			'guest_path',
		]


class NetworkForm(ModelForm):
	class Meta:
		model = Network
		fields = [
			'name',
			'external',
		]
		# these will be set programatically
		exclude = [
			'name',
		]


class EnvironmentVariableForm(ModelForm):
	class Meta:
		model = EnvironmentVariable
		fields = [
			'name',
			'value',
		]


class LabelForm(ModelForm):
	class Meta:
		model = Label
		fields = [
			'name',
			'value',
		]
		# all fields will be set programatically
		exclude = fields
