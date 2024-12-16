from django.shortcuts import render
from django.views.generic import ListView
from .models import Site

# Create your views here.
class SitesListView(ListView):
	model = Site
	template_name = 'sites/list.html'
