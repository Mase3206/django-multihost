from django.views.generic import ListView
from sites.models import Site


class HomepageView(ListView):
	model = Site
	template_name = 'home.html'
