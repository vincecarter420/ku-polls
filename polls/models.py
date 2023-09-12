import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=False, )
    end_date = models.DateTimeField('date ended', null=True)

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def is_published(self):
        return self.pub_date <= timezone.now()

    def can_vote(self):
        if self.end_date is None:
            return self.is_published
        return self.is_published and self.end_date >= timezone.now()

    def __str__(self):
        return self.question_text
    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        '''count the votes for this choice.'''
        return self.vote_set.count

    def __str__(self):
        return self.choice_text
    
class Vote(models.Model):
    """Record a choice for a question made by a user."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        pass