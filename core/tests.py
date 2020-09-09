import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question
from django.urls import reverse


def create_question(question_text=None, offset_days=0):
    date_published = timezone.now() + datetime.timedelta(days=offset_days)
    question = Question.objects.create(date_published=date_published)
    if question_text is None:
        question.question_text = 'Question #' + str(question.id)
    else:
        question.question_text = question_text
    question.save()
    return question


class QuestionModelTest(TestCase):

    def test_was_published_recently_is_false_for_future_question(self):
        future_question = create_question(offset_days=30)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_is_false_for_question_older_than_one_day(self):
        old_question = create_question(offset_days=-2)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_is_true_for_question_published_yesterday(self):
        yesterday = timezone.now(
        ) - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(date_published=yesterday)
        self.assertTrue(recent_question.was_published_recently())


class QuestionPollsListTests(TestCase):
    def test_when_no_questions_display_a_message(self):
        response = self.client.get(reverse('core:polls_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['last_questions_list'], [])
        self.assertContains(response, "No polls are available.")

    def test_question_with_pub_date_in_the_past_are_displayed(self):
        create_question(question_text="Past question.", offset_days=-30)
        response = self.client.get(reverse('core:polls_list'))
        self.assertQuerysetEqual(response.context['last_questions_list'], [
                                 '<Question: Past question.>'])
        self.assertEqual(len(response.context['last_questions_list']), 1)

    def test_question_with_pub_date_in_the_future_are_not_displayed(self):
        create_question(question_text="Future question.", offset_days=30)
        response = self.client.get(reverse('core:polls_list'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['last_questions_list'], [])

    def test_question_with_pub_date_in_the_past_are_displayed_future_not(self):
        create_question(question_text="Past question.", offset_days=-30)
        create_question(question_text="Future question.", offset_days=30)
        response = self.client.get(reverse('core:polls_list'))
        self.assertQuerysetEqual(
            response.context['last_questions_list'],
            ['<Question: Past question.>'])

    def test_multiple_questions_are_displayed(self):
        create_question(question_text="Past question 1.", offset_days=-30)
        create_question(question_text="Past question 2.", offset_days=-5)
        response = self.client.get(reverse('core:polls_list'))
        self.assertQuerysetEqual(
            response.context['last_questions_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>'])


class QuestionDetailViewTests(TestCase):
    def test_detail_of_future_question_returns_404(self):
        future_question = create_question(
            question_text='Future question.', offset_days=5)
        url = reverse('core:poll_detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_of_past_question_displays_question_text(self):
        past_question = create_question(
            question_text='Past Question.', offset_days=-5)
        url = reverse('core:poll_detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
