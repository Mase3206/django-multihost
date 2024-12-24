from django.forms import BaseModelForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.contrib.auth.mixins import (
	AccessMixin, # control what happens if 403
	LoginRequiredMixin, # ensure user is logged in
    UserPassesTestMixin, # extra conditions that, if failed, throw a 403
)

from account.models import CustomUser
from django.conf import settings
from django.urls import reverse_lazy, reverse

# from revproxy.views import ProxyView
from django.views.decorators.csrf import csrf_exempt
# from proxy.views import proxy_view

from .models import Site
from .forms import SiteForm

from account.models import CustomUser

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


class SiteCreationView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	form_class = SiteForm
	login_url = settings.LOGIN_URL
	template_name = 'sites/create.html'
	success_url = reverse_lazy('sites:list')
	permission_denied_message = f'You are not permitted to create new sites.'

	def test_func(self) -> bool | None:
		"""
		Ensure the user is permitted to create sites.
		"""
		return self.request.user.has_perm('sites.add_site') #type:ignore


class SiteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Site
	form_class = SiteForm
	login_url = settings.LOGIN_URL
	template_name = 'sites/update.html'

	@property
	def this_object(self) -> Site:
		return super().get_object(self.get_queryset()) #type:ignore

	def test_func(self) -> bool | None:
		"""
		Ensure the user is either an admin or is associated with the site.
		"""

		this_user = CustomUser.objects.get(pk=self.request.user.pk)

		return (
			self.request.user.has_perm('sites.change_site') or #type:ignore
			this_user.associated_site == self.this_object
		)
	
	def get_success_url(self) -> str:
		return reverse(
			'sites:detail',
			kwargs = { 'pk': self.this_object.pk }
		)



class SiteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Site
	# form_class = SiteForm
	login_url = settings.LOGIN_URL
	template_name = 'sites/delete.html'
	success_url = reverse_lazy('sites:list')

	def test_func(self) -> bool | None:
		"""
		Ensure the user is permitted to delete sites.
		"""
		return self.request.user.has_perm('sites.delete_site') #type:ignore
	
	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		context['site_owners'] = CustomUser.objects.filter(associated_site=self.get_object())
		return context



class SiteJoinView(LoginRequiredMixin, UpdateView):
	model = CustomUser
	fields = ['associated_site']
	exclude = ['associated_site']
	login_url = settings.LOGIN_URL
	template_name = 'sites/join.html'

	def get_context_data(self, **kwargs) -> dict:
		context = super().get_context_data(**kwargs)
		context['site'] = Site.objects.get(pk=self.kwargs['pk'])
		return context
	
	def get_success_url(self) -> str:
		return reverse('sites:detail', kwargs={'pk': self.kwargs['pk']})
	
	def get_form(self, form_class: BaseModelForm | None = None) -> BaseModelForm:
		"""
		Set the associated_site field (hidden) to link the PK'd site to the user account that is currently signed in. 

		This seems to be a critical step.
		"""
		form = super().get_form(form_class) #type:ignore
		form.initial['associated_site'] = Site.objects.get(pk=self.kwargs['pk'])

		return form
	
	def form_valid(self, form: BaseModelForm) -> HttpResponse:
		"""
		Set the that the associated_site field (hidden) to the PK'd site (again, which is required for some reason) on signed-in user and save the user.
		
		If, after doing this, the field is stil not set correctly, an AssertionError will be raised.
		
		If not, then save the form.
		"""
		obj: CustomUser = form.save(commit=False)

		obj.associated_site = Site.objects.get(pk=self.kwargs['pk'])
		obj.save()

		assert obj.associated_site == Site.objects.get(pk=self.kwargs['pk']), 'obj.associated_site field was not correctly set!'

		# obj = CustomUser.objects.get(pk=self.request.user.pk)
		# site = Site.objects.get(pk=self.kwargs['pk'])
		# obj.associated_site = site
		# obj.save(update_fields=['associated_site'])

		form.save()

		return super().form_valid(form)



def site_deployment_husk_view(request, pk: int = ...): #type:ignore
	"""
	This FBV doesn't render anything. It's sole purpose is to be something the URL dispatcher can point to in the urlconf. Traefik is configured to look for this URL and take over from there doing its proxy/path-strip thing.
	"""
	return HttpResponse()




# def get_hostname_parts() -> list[str]:
# 	hs = ['', '']
# 	hs = settings.HOSTNAME.split(':')

# 	if len(hs) > 1:
# 		if settings.HTTPS:
# 			hs[1] = '443'
# 		else:
# 			hs[1] = '80'
# 	return hs

# class SiteDeploymentView(View):
# 	pass
# 	model = Site
	# hostname_parts = get_hostname_parts()
	# if hostname_parts[1] == settings.DEPLOY_START_PORT:
	# 	raise ImproperlyConfigured('The DEPLOY_START_PORT must be set to a port other than the used by this public-facing frontend.')

	# base_url = 'https' if settings.HTTPS else 'http' + '://' + hostname_parts[0]
	# upstream = base_url + f':{settings.DEPLOY_START_PORT + 1}'


	# def upstream(self, value):
	# 	# self._upstream = self.base_url + f':{settings.DEPLOY_START_PORT + self.get_object().pk}'
	# 	self._upstream = self.base_url + f':{settings.DEPLOY_START_PORT + 1}'
	# 	self.kwargs.pop('pk')
		# url = self.base_url + f':{settings.DEPLOY_START_PORT + site.pk}'

# 	def dispatch(self, request, path):
# 		return super().dispatch(request, path)


# def site_deployment_proxy(request, path, **kwargs):
# 	extra_requests_args = {...}
# 	hostname_parts = get_hostname_parts()
# 	base_url = 'https' if settings.HTTPS else 'http' + '://' + hostname_parts[0]

# 	remote_url = base_url + str(settings.DEPLOY_START_PORT + kwargs.pop('pk'))
# 	return proxy_view(request, remote_url, extra_requests_args)