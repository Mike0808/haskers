from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            login='will',
            email='will@email.com',
            password='testpass123',
        )
        self.assertEqual(user.login, 'will')
        self.assertEqual(user.email, 'will@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            login='superadmin',
            email='superadmin@email.com',
            password='testpass123',

        )
        self.assertEqual(admin_user.login, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignupPageTests(TestCase):
    login = 'newuser'
    email = 'newuser@email.com'
    password = 'testpass123'
    avatar = 'avatar.png'

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        new_user = get_user_model().objects.create_user(email=
                                                        self.email, password=self.password, login=self.login)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()
                         [0].login, self.login)
        self.assertEqual(get_user_model().objects.all()
                         [0].email, self.email)


class SettingsPageTests(TestCase):

    def setUp(self):
        self.usern = CustomUser.objects.create_superuser(
            login='zodd',
            email='zodd@email.com',
            password='testpass123',
        )
        self.response = self.client.login(email='zodd@email.com', password='testpass123')
        self.url = reverse('settings')

    def test_settings_template(self):
        self.response = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/settings.html')
        self.assertContains(self.response, 'Settings')
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_settings_user_update(self):
        post_data = {
            'email': self.usern.email,
            'login': self.usern.login,
        }
        response = self.client.post(reverse('settings'), {"email": 'email@email.com', "login": "something"})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.usern.refresh_from_db()
        self.assertEqual(CustomUser.objects.all()[0].login, 'something')
