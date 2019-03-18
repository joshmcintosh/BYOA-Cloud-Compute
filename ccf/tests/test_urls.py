from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse


class TestAccountsPage(TestCase):
    def test_get_login(self):
        client = Client()
        response = self.client.get("http://127.0.0.1:8000/accounts/login/")
        assert response.status_code == 200

    def test_landing_redirect(self):
        client = Client()
        response = self.client.get("http://127.0.0.1:8000", follow=True)
        SimpleTestCase().assertRedirects(response, "/accounts/login/?next=/")

    def test_logged_in_user_directs_to_homepage(self):
        client = Client()
        user = User.objects.create_user(username="testuser", password="12345")

        logged_in = client.login(username="testuser", password="12345")
        response = client.get("http://127.0.0.1:8000", follow=True)

        self.assertTrue(logged_in)
        self.assertTemplateUsed(response, "tmp_home.html")


class TestSignupPage(TestCase):
    def test_get_signup(self):
        client = Client()
        response = client.get("http://127.0.0.1:8000/accounts/signup/")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "signup.html")

    def test_get_signup_by_name(self):
        client = Client()
        response = client.get(reverse("signup"), follow=True)

        assert response.status_code == 200
        self.assertTemplateUsed(response, "signup.html")
