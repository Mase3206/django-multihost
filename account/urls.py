from django.urls import path
from .views import SignUpView
from django.views.generic import TemplateView
from django.contrib.auth.views import (
	LoginView,
	PasswordChangeView,
	PasswordResetConfirmView,
	PasswordResetView,
)

urlpatterns = [
	# custom
	path('signup/', SignUpView.as_view(), name='signup'),

	# modified
	path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
	path('password_change/', PasswordChangeView.as_view(template_name='account/password_change_form.html'), name='password_change'),
	path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
	path('password_reset/', PasswordResetView.as_view(template_name='account/password_reset_form.html'), name='password_reset'),

	# no context, just rendering
	path('logged-out/', TemplateView.as_view(template_name='account/logged_out.html'), name='logged_out'),
]
