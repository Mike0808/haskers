from django.contrib.auth import get_user_model
from .models import Question
from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import QuestionListView


class QuestionListTests(SimpleTestCase):
    databases = '__all__'

    def setUp(self):
        url = reverse('questions:question_list')
        self.response = self.client.get(url)

    def test_question_list_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_question_homepage_template(self):
        self.assertTemplateUsed(self.response, 'questions/question_list.html')

    def test_question_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Questions')

    def test_question_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_question_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            QuestionListView.as_view().__name__
        )


class QuestionCreateTests(TestCase):
    user = get_user_model()

    def setUp(self):
        self.usern = self.user.objects.create_superuser(
            login='zodd',
            email='zodd@email.com',
            password='testpass123',
        )
        self.response = self.client.login(email='zodd@email.com', password='testpass123')
        self.question = Question.objects.create(
            title='How are you?',
            author=self.usern,
            text='What about some question?',
        )

    def test_question_listing(self):
        self.assertEqual(f'{self.question.title}', 'How are you?')
        self.assertEqual(f'{self.question.author}', self.usern.email)
        self.assertEqual(f'{self.question.text}', 'What about some question?')

    def test_question_list_view(self):
        response = self.client.get(reverse('questions:question_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'How are you?')
        self.assertTemplateUsed(response, 'questions/question_list.html')

    def test_question_detail_view(self):
        response = self.client.get(self.question.get_absolute_url())
        no_response = self.client.get('/questions/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'How are you?')
        self.assertTemplateUsed(response, 'questions/question_detail.html')
