from django.urls import path
from .views import (
	SitesListView, 
	SiteDetailView, 
	SiteCreationView, 
	SiteUpdateView,
	SiteDeleteView,
	site_deployment_husk_view
)

from django.views.generic import View

app_name = 'sites'
urlpatterns = [
	path('', SitesListView.as_view(), name='list'),
	path('<int:pk>/', SiteDetailView.as_view(), name='detail'),
	path('create/', SiteCreationView.as_view(), name='create'),
	path('<int:pk>/update/', SiteUpdateView.as_view(), name='update'),
	path('<int:pk>/delete/', SiteDeleteView.as_view(), name='delete'),
	path('<int:pk>/view/', site_deployment_husk_view, name='view'), # this is just here to 
]
