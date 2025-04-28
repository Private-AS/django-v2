from django import forms
from .models import Poll, Question, Choice

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['poll_name']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']