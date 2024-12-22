from django.forms import ModelForm

from deploy.models.compose import (
	Deployment,
)


class DeploymentWizardForm(ModelForm):
	class Meta:
		model = Deployment
		fields = [
			'git_repo',
			'sgi_server',
			'database', 
		]
		# these will be set programatically
		exclude = [
			'sgi_server',
			'database',
		]
