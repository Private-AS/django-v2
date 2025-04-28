from django.contrib import admin
from django.contrib.auth.models import User

from .models import Poll, Question, Choice, PollSubmission

# Register your models here.

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(PollSubmission)

