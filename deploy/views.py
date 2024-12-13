from django.views.generic import TemplateView


class BasicHomepageView(TemplateView):
	template_name = 'base.html'
