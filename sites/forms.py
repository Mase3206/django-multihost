from django.forms import ModelForm, Textarea

from .models import Site


class SiteForm(ModelForm):
	class Meta:
		model = Site
		fields = [
			'name',
			'path',
			'remote_repo',
			'description',
			'description_brief',
			'use_bundled_db'
		]
		widgets = {
			'description_brief': Textarea(attrs={'rows': 3}),
			'description': Textarea(attrs={'rows': 6}),
		}

		help_texts = {
			'use_bundled_db': 'Use a bundled Postgres database instead of a manually-configured one.',
			'path': 'Not sure what I thought this would be used for. It is currently unused.',
			'description': 'CommonMark-compliant Markdown formatting is accepted.'
		}