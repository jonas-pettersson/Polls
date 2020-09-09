import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTest(TestCase):

    def test_was_published_recently_is_false_for_future_question(self):

        thirty_days_into_the_future = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(date_published=thirty_days_into_the_future)

        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_is_false_for_question_older_than_one_day(self):

        yesterday_minus_one_second = timezone.now(
        ) - datetime.timedelta(days=1, seconds=1)
        old_question = Question(date_published=yesterday_minus_one_second)

        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_is_true_for_question_published_yesterday(self):

        yesterday = timezone.now(
        ) - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(date_published=yesterday)

        self.assertTrue(recent_question .was_published_recently())
