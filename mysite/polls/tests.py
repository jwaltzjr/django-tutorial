import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from . import models

class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions
        whose pub_date is older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=1.1)
        future_question = models.Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions
        whose pub_date is within the last day
        """
        time = timezone.now() - datetime.timedelta(days=0.9)
        future_question = models.Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions
        whose pub_date is in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = models.Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

class QuestionViewTests(TestCase):

    def test_index_view_with_no_questions(self):
        """
        If no questions exist, a message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            []
        )

    def test_index_view_with_past_question(self):
        """
        Questions with a pub_date in the past should be displayed.
        """
        create_question(question_text='Past Question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past Question>']
        )

    def test_index_view_with_future_question(self):
        """
        Questions with a pub_date in the future should not be dispayed.
        """
        create_question(question_text='Future Question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            []
        )


    def test_index_view_with_future_and_past_questions(self):
        """
        If both past and future questions exists, only past questions
        should be displayed.
        """
        create_question(question_text='Future Question', days=30)
        create_question(question_text='Past Question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past Question>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The index page may display multiple questions.
        """
        create_question(question_text='Past Question 1', days=-30)
        create_question(question_text='Past Question 2', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past Question 2>','<Question: Past Question 1>']
        )

class QuestionIndexDetailTests(TestCase):

    def test_detail_view_with_future_question(self):
        """
        The detail view for a future question should return a 404
        """
        future_question = create_question(question_text='Future Question', days=5)
        url = reverse('polls:detail', args=[future_question.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_past_question(self):
        """
        The detail view for a past question should display
        the question's text
        """
        past_question = create_question(question_text='Future Question', days=-5)
        url = reverse('polls:detail', args=[past_question.id])
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

def create_question(question_text, days):
    """
    Creates a question with the given "question_text" and
    published the given number of 'days' offset from now.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return models.Question.objects.create(question_text=question_text, pub_date=time)