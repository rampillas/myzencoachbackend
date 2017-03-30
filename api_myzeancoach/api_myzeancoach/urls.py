# -*- coding: utf-8 -*-
from django.conf.urls import patterns,include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(pattern_name='api_root', permanent=False, url='/admin')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^', include('users.urls')),
    url(r'^essential_information/', include('essential_information.urls')),
    url(r'^minfulness/', include('minfulness.urls')),
    url(r'^personalization/', include('personalization.urls')),
    url(r'^solutions/', include('solutions.urls')),
    url(r'^freetime/', include('freetime.urls')),
    url(r'^login', 'users.views.login',name="login"),
    url(r'^password-recovery', 'users.views.recover_password',name="password-recovery"),
)
