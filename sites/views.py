from django.views.generic import ListView, DetailView
from .models import Site

# Create your views here.
class SitesListView(ListView):
	model = Site
	template_name = 'sites/list.html'


class SiteDetailView(DetailView):
	model = Site
	template_name = 'sites/detail.html'

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		context['current_pk'] = self.kwargs.get('pk')
		return context
