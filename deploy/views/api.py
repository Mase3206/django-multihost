from subprocess import CalledProcessError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from deploy.models import Deployment
from deploy.serializers import DeploymentSerializer

from deploy.tasks import api


class DeploymentAPIView(APIView):
	# make sure user is authenticated
	# authentication_classes = [JWTAuthentication, JWTTokenUserAuthentication]
	authentication_classes = [
		SessionAuthentication,
		BasicAuthentication,
	]
	permission_classes = [IsAuthenticated]
	
	
	def get(self, request, deploy_id, *args, **kwargs):
		"""
		Get info about PK'd deployment.
		"""
		depl = Deployment.objects.get(pk=deploy_id)
		if not depl:
			return Response(
				{'res': 'Deployment with given id does not exist.'},
				status=status.HTTP_400_BAD_REQUEST
			)
		serializer = DeploymentSerializer(depl, many=False)
		return Response(serializer.data, status=status.HTTP_200_OK)


	def put(self, request, deploy_id, *args, **kwargs):
		"""
		Update PK'd deployment's status (online, offline).
		"""

		depl = Deployment.objects.get(pk=deploy_id)
		if not depl:
			return Response(
				{'res': 'Deployment with given id does not exist.'},
				status=status.HTTP_400_BAD_REQUEST
			)
		
		try:
			api.parse_actions(
				depl,
				api.Actions(**request.data)
			)
			return Response(
				{'res': 'Successfully completed all actions.'},
				status=status.HTTP_200_OK
			)
		except CalledProcessError as e:
			raise e
			return Response(
				{'res': 'One or more actions failed.'},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
