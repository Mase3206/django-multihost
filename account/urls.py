from django.urls import path
from .views import SignUpView, SiteGroupCreateView

urlpatterns = [
	path('user/signup/', SignUpView.as_view(), name='signup'),
	path('group/create/', SiteGroupCreateView.as_view(), name='group_create'),
]
