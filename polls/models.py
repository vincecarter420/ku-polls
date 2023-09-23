import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    """
    Represents a poll question.

    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime.datetime): The date the question was published.
        end_date (datetime.datetime, optional): The date the question ended (if specified).

    Methods:
        was_published_recently(): Checks if the question was published within the last day.
        is_published(): Checks if the question is currently published.
        can_vote(): Checks if users can vote on the question.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('date ended', null=True)

    def was_published_recently(self):
        """
        Returns True if the question was published within the last day, False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def is_published(self):
        """
        Returns True if the question is currently published, False otherwise.
        """
        return self.pub_date <= timezone.now()

    def can_vote(self):
        """
        Returns True if users can vote on the question, False otherwise.
        """
        if self.end_date is None:
            return self.is_published()
        return self.is_published() and self.end_date >= timezone.now()

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    """
    Represents a choice for a poll question.

    Attributes:
        question (Question): The question to which this choice belongs.
        choice_text (str): The text of the choice.

    Properties:
        votes (int): The number of votes for this choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        """
        Returns the number of votes for this choice.
        """
        return self.vote_set.count()

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    """
    Represents a vote made by a user for a specific choice in a question.

    Attributes:
        user (User): The user who made the vote.
        choice (Choice): The choice that was voted for.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
