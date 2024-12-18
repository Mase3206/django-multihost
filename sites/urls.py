from django.urls import path
from .views import SitesListView, SiteDetailView, SiteDeploymentView

app_name = 'sites'
urlpatterns = [
	path('', SitesListView.as_view(), name='list'),
	path('<int:pk>/', SiteDetailView.as_view(), name='detail'),
	path('<int:pk>/deployment/', SiteDeploymentView.as_view(), name='deployment')
]
