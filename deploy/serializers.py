from rest_framework.serializers import ModelSerializer
from .models import Deployment

# class DeploymentStatusChangeSerializer(ModelSerializer):
# 	"""
# 	This is used to change the status of the 
# 	"""
# 	class Meta:
# 		model = Deployment
# 		fields = ['online']


class DeploymentSerializer(ModelSerializer):
	class Meta:
		model = Deployment
		fields = [
			'git_repo',
			# 'online',
			# 'modified',
		]
