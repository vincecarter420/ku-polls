import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    """
    Represents a poll question.
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=False)
    end_date = models.DateTimeField('date ended', null=True)

    def was_published_recently(self):
        """
        Returns True if the question was published within the last day.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def is_published(self):
        """
        Returns True if the question is currently published.
        """
        return self.pub_date <= timezone.now()

    def can_vote(self):
        """
        Returns True if voting is allowed for this question.
        """
        if self.end_date is None:
            return self.is_published
        return self.is_published() and self.end_date >= timezone.now()

    def __str__(self):
        return self.question_text
    

class Choice(models.Model):
    """
    Represents a choice for a poll question.
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
