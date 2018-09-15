
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30) #Use the datetime module to make a date in the future
        future_question = Question(pub_date=time) #Create a new question
        self.assertIs(future_question.was_published_recently(), False) #Create an assertion using the test case Class

