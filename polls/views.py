from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice, Poll
# Create your views here.

def home(request):
    return render(request, 'polls/home.html', {})