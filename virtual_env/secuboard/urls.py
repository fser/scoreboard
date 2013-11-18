from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from secuboard.models import Challenge, Response

from secuboard.views import ChallengeList, ChallengeDetail


urlpatterns = patterns('',
                       url(r'^$', ChallengeList.as_view()),
                       url(r'^(?P<pk>\d+)/', ChallengeDetail.as_view(), name='toto'),
                       url(r'^hello/', TemplateView.as_view(template_name="test.html")),
)
