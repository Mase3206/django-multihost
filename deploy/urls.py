from django.urls import path, include

from .views.quickcreate import DeploymentQuickcreateCreateView

from .views.api import DeploymentAPIView

app_name = 'deploy'
urlpatterns = [
	path('quickcreate/<int:site_pk>/', DeploymentQuickcreateCreateView.as_view(), name='quickcreate'),
	path('api/<int:deploy_id>/', DeploymentAPIView.as_view()),
]