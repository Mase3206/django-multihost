from django.views.generic import ListView, DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# from revproxy.views import ProxyView
from django.views.decorators.csrf import csrf_exempt
# from proxy.views import proxy_view

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



def get_hostname_parts() -> list[str]:
	hs = ['', '']
	hs = settings.HOSTNAME.split(':')

	if len(hs) > 1:
		if settings.HTTPS:
			hs[1] = '443'
		else:
			hs[1] = '80'
	return hs

class SiteDeploymentView(View):
	pass
# 	model = Site
	# hostname_parts = get_hostname_parts()
	# if hostname_parts[1] == settings.DEPLOYMENT_START_PORT:
	# 	raise ImproperlyConfigured('The DEPLOYMENT_START_PORT must be set to a port other than the used by this public-facing frontend.')

	# base_url = 'https' if settings.HTTPS else 'http' + '://' + hostname_parts[0]
	# upstream = base_url + f':{settings.DEPLOYMENT_START_PORT + 1}'


	# def upstream(self, value):
	# 	# self._upstream = self.base_url + f':{settings.DEPLOYMENT_START_PORT + self.get_object().pk}'
	# 	self._upstream = self.base_url + f':{settings.DEPLOYMENT_START_PORT + 1}'
	# 	self.kwargs.pop('pk')
		# url = self.base_url + f':{settings.DEPLOYMENT_START_PORT + site.pk}'

# 	def dispatch(self, request, path):
# 		return super().dispatch(request, path)


# def site_deployment_proxy(request, path, **kwargs):
# 	extra_requests_args = {...}
# 	hostname_parts = get_hostname_parts()
# 	base_url = 'https' if settings.HTTPS else 'http' + '://' + hostname_parts[0]

# 	remote_url = base_url + str(settings.DEPLOYMENT_START_PORT + kwargs.pop('pk'))
# 	return proxy_view(request, remote_url, extra_requests_args)