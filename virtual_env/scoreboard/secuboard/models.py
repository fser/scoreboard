from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Challenge(models.Model):
	starts_at   = models.DateTimeField()
	ends_at     = models.DateTimeField()
	title       = models.CharField(max_length=200)
	challenge   = models.CharField(max_length=2000)
	answer      = models.CharField(max_length=50)
	linked_file = models.FileField(upload_to='attached_files', null=True, blank=True)

	def __unicode__(self):
		return self.title

class Response(models.Model):
	user      = models.ForeignKey(User,)
	challenge = models.ForeignKey(Challenge)
	date      = models.DateTimeField()

	def __unicode__(self):
		return '%s at %s' % (self.user, self.date)

class ChallengeAdmin(admin.ModelAdmin):
    pass

class ResponseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Response, ResponseAdmin)
	
