from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = CustomUser
		fields = [
			'first_name',
			'last_name',
			'username',
			'email',
			'associated_site',
			'github_username',
			'password1',
			'password2',
		]
		help_texts = {
			'username': 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. You will use this to sign into this site.',
			'github_username': 'This is used to help keep track of site access permissions.'
		}


# class CustomUserChangeForm(UserChangeForm):
# 	class Meta:
# 		model = CustomUser
# 		fields = [
# 			'username',
# 			'email',
# 			'associated_site',
# 			'github_username',
# 		]