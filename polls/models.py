from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Poll(models.Model):
    poll_id = models.AutoField(primary_key=True)
    poll_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    is_submitted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_by', null=True, blank=True)

    def __str__(self):
        return self.poll_name

class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, default=1)
    pub_date = models.DateTimeField('date published')
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

