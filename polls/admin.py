from django.contrib import admin
from .models import Poll, Question, Choice
# Register your models here.

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
