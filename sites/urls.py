from django.urls import path
from .views import (
	SitesListView, 
	SiteDetailView, 
	SiteCreationView, 
	SiteUpdateView,
	SiteDeleteView
)

from django.views.generic import View

app_name = 'sites'
urlpatterns = [
	path('', SitesListView.as_view(), name='list'),
	path('<int:pk>/', SiteDetailView.as_view(), name='detail'),
	path('create/', SiteCreationView.as_view(), name='create'),
	path('<int:pk>/update/', SiteUpdateView.as_view(), name='update'),
	path('<int:pk>/delete/', SiteDeleteView.as_view(), name='delete'),
	path('<int:pk>/view/', View.as_view(), name='view')
]
