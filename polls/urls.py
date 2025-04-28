from django.urls import path
from . import views
from register.views import delete_account

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:id>', views.poll, name='poll'),
    path('save', views.save, name='save'),
    path('your_polls', views.your_polls, name='your_polls'),
    path('your_answers', views.your_answers, name='your_answers'),
    path('your_account', views.your_account, name='your_account'),
    path('delete_account', delete_account, name='delete_account'),
    path('<int:id>/answers', views.answers, name='answers'),
    path('create', views.create, name='create'),
]