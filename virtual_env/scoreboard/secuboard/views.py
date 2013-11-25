# toremove
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.utils import timezone
from django.utils.decorators import method_decorator

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext




# Django generic views
from django.views.generic import ListView
from django.views.generic import DetailView

# Application models
from secuboard.models import Challenge, Response


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
            scores.append({'username': current_user, 
	    		   'score': sum([rsp.challenge.reward for rsp in user_responses]), 
			   'epreuves': ','.join([str(rsp.challenge.id) for rsp in user_responses]),})
        return sorted(scores, key=lambda elt : elt['score'], reverse=True)

def validate(request, id):
	if not request.user.is_authenticated():
		return HttpResponse("Must be authenticated")
	if request.method == 'POST':
		ans = request.POST['answer']
		chal = Challenge.objects.get(pk=int(id))
		if chal.answer == ans:
			if (Response.objects.all().filter(user=request.user, challenge=chal).exists()):
				return HttpResponse("Deja valide")
			r = Response(user=request.user, challenge=chal)
			r.save()
			return render_to_response('submit.html', {'flag_valid': True},context_instance=RequestContext(request))
		else:
			return render_to_response('submit.html', {'flag_valid': False},context_instance=RequestContext(request))
	else:
		return HttpResponse("Invalid request")
