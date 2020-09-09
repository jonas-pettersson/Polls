import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTest(TestCase):

    @staticmethod
    def create_question(question_text=None, offset_days=0):

        date_published = timezone.now() + datetime.timedelta(days=offset_days)

        question = Question.objects.create(date_published=date_published)
        if question_text is None:
            question.question_text = 'Question #' + str(question.id)
        else:
            question.question_text = question_text
        question.save()

        return question

    def test_was_published_recently_is_false_for_future_question(self):

        future_question = self.create_question(offset_days=30)

        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_is_false_for_question_older_than_one_day(self):

        old_question = self.create_question(offset_days=-2)

        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_is_true_for_question_published_yesterday(self):

        yesterday = timezone.now(
        ) - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(date_published=yesterday)

        self.assertTrue(recent_question .was_published_recently())
