from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, SiteGroupCreationForm

class SignUpView(CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'account/signup.html'


class SiteGroupCreateView(CreateView):
	form_class = SiteGroupCreationForm
	success_url = reverse_lazy('home')
	template_name = 'groups/create.html'
