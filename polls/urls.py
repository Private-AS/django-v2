from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('answers', views.answers, name='answers'),
   # path('poll', views.poll, name='poll'),
  #  path('save', views.save, name='save'),
]