from django.forms import ModelForm, Textarea

from .models import Site
from account.models import CustomUser


class SiteForm(ModelForm):
	class Meta:
		model = Site
		fields = [
			'name',
			'description',
			'description_brief',
		]
		widgets = {
			'description_brief': Textarea(attrs={'rows': 3}),
			'description': Textarea(attrs={'rows': 12}),
		}

		help_texts = {
			# 'use_bundled_db': 'Use a bundled Postgres database instead of a manually-configured one.',   # TODO - move this to deploy.forms
			'description': 'CommonMark-compliant Markdown formatting is accepted.'
		}


class UserJoinForm(ModelForm):
	class Meta:
		model = CustomUser
		fields = [
			'associated_site'
		]
		exclude = fields