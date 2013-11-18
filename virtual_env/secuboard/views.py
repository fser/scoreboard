# toremove
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.utils import timezone
from django.utils.decorators import method_decorator

# Django generic views
from django.views.generic import ListView
from django.views.generic import DetailView

# Application models
from secuboard.models import Challenge, Response

import datetime

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ChallengeList(LoginRequiredMixin, ListView):
    model = Challenge
    context_object_name = 'challenge_list'
    queryset = Challenge.objects.all().filter(starts_at__lte=timezone.now(),ends_at__gte=timezone.now())

class ChallengeDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'challenge'
    queryset = Challenge.objects.all().filter(starts_at__lte=timezone.now(),ends_at__gte=timezone.now())


class Scoreboard(ListView):
    def get_queryset(self):
        scores = []
        users = User.objects.all()
        for current_user in users:
            user_responses = Response.objects.filter(user=current_user)
            scores.append({'username': current_user, 'score': sum([rsp.challenge.reward for rsp in user_responses])})
        return scores
