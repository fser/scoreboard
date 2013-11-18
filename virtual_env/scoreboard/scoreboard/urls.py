from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

import scoreboard
from secuboard.views import Scoreboard

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Login stuffs
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',  {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),

    # Static pages
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^about/$', TemplateView.as_view(template_name="about.html")),
    url(r'^contact/$', TemplateView.as_view(template_name="contact.html")),

    # Challenges related urls
    url(r'^scoreboard/$', Scoreboard.as_view(template_name="scoreboard.html")),
    url(r'^challenge/', include('secuboard.urls')),

    # Admin related urls
    url(r'^admin/', include(admin.site.urls)),
)
