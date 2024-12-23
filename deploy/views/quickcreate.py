from typing import Any
from django.http import HttpResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy

from django.shortcuts import redirect

from deploy.tasks.quickcreate import create


# from deploy.forms import (
# 	# DeploymentQuickcreateForm,
# 	# GunicornQuickcreateForm,
# 	# PostgresQuickcreateForm,
# 	VolumeForm,
# 	NetworkForm,
# 	EnvironmentVariableForm,
# 	LabelForm,
# )

from deploy.forms.quickcreate import QuickcreateCreationMultiForm

class DeploymentQuickcreateCreateView(CreateView):
	form_class = QuickcreateCreationMultiForm #type:ignore
	success_url = reverse_lazy('home')
	template_name = 'deploy/quickcreate/create.html'

	def get_context_data(self, **kwargs) -> dict[str, Any]:
		context = super().get_context_data(**kwargs)
		context['site_pk'] = self.kwargs['site_pk']
		return context

	def form_valid(self, form: QuickcreateCreationMultiForm) -> HttpResponse:
		context = self.get_context_data()
		create(form, context)
		return redirect(self.success_url)
