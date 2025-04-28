from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Poll(models.Model):
    poll_id = models.AutoField(primary_key=True)
    poll_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')

    def __str__(self):
        return self.poll_name

class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, default=1)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class PollSubmission(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('poll', 'user')  # Ensure a user can submit a poll only once