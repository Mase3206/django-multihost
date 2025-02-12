"""
URL configuration for deploy project.

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings

from debug_toolbar.toolbar import debug_toolbar_urls

from .views import HomepageView

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api-auth/', include('rest_framework.urls')),

	path('account/', include('account.urls')),
	path('account/', include('django.contrib.auth.urls')),

	path('sites/', include('sites.urls')),
	path('deploy/', include('deploy.urls')),
	path('', HomepageView.as_view(), name='home'),
]

if settings.DEBUG == True:
	urlpatterns += debug_toolbar_urls()
