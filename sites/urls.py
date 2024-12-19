from django.urls import path
from .views import SitesListView, SiteDetailView, SiteCreationView

app_name = 'sites'
urlpatterns = [
	path('', SitesListView.as_view(), name='list'),
	path('<int:pk>/', SiteDetailView.as_view(), name='detail'),
	path('create/', SiteCreationView.as_view(), name='create')
	# path('<int:pk>/deployment/', SiteDeploymentView.as_view(), name='deployment')
]
