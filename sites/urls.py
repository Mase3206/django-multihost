from django.urls import path
from ..deploy.views import SitesListView

appname = 'sites'
urlpatterns = [
	path('', SitesListView.as_view(), name='list'),
	path('<int:pk>/', SiteDetailView.as_view(), name='detail')
]
