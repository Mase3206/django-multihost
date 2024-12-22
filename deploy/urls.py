from django.urls import path, include

from .views.quickcreate import DeploymentQuickcreateCreateView

app_name = 'deploy'
urlpatterns = [
	path('quickcreate/<int:site_pk>/', DeploymentQuickcreateCreateView.as_view(), name='quickcreate')
]