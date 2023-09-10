import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    '''test is_published()'''
    def test_future_pub_date(self):
        '''return False if pub_date is future date'''
        time = timezone.now() + datetime.timedelta(days=10)
        test = Question(pub_date=time)
        self.assertFalse(test.is_published())
    
    def test_current_pub_date(self):
        '''return True if pub_date is current date'''
        time = timezone.now()
        test = Question(pub_date=time)
        self.assertTrue(test.is_published())
    
    def test_past_pub_date(self):
        '''return True if pub_date is past date but not over end_date'''
        time = timezone.now() - datetime.timedelta(days=10)
        test = Question(pub_date=time)
        self.assertTrue(test.is_published())

    '''test can_vote()'''
    def test_current_date(self):
        '''return True if client can vote the poll which in the current date'''
        test = Question(pub_date=timezone.now())
        self.assertTrue(test.can_vote())

    def test_if_over_pub(self):
        '''return True if client can vote the poll which pub_date is over'''
        pub = timezone.now() - datetime.timedelta(days=5)
        test = Question(pub_date=pub)
        self.assertTrue(test.can_vote())

    def test_if_over_end(self):
        '''return False if client cannot vote the poll which over end date'''
        pub = timezone.now() - datetime.timedelta(days=5)
        end = timezone.now() - datetime.timedelta(days=10)
        test = Question(pub_date=pub, end_date=end)
        self.assertFalse(test.can_vote())
    
    def test_if_not_over_end(self):
        '''return True if client can vote the poll which not over end date'''
        end = timezone.now() + datetime.timedelta(days=5)
        test = Question(pub_date=timezone.now(), end_date=end)
        self.assertTrue(test.can_vote())
    

class QuestionIndexViewTests(TestCase):

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)