from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
	class Meta:
		model = CustomUser
		fields = [
			'username',
			'email', 
		]


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = [
			'username',
			'email', 
		]


class SiteGroupCreationForm(ModelForm):
	class Meta:
		model = Group
		exclude = []
