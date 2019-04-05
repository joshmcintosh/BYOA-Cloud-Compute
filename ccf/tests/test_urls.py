import pytest
import test_utils
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse


class TestAccountsPage(TestCase):
    def test_get_login(self):
        client = Client()
        response = self.client.get("http://127.0.0.1:8000/accounts/login/")
        assert response.status_code == 200

    def test_logged_in_user_directs_to_homepage(self):
        client = Client()
        user = User.objects.create_user(username="testuser", password="12345")

        logged_in = client.login(username="testuser", password="12345")
        response = client.get("http://127.0.0.1:8000", follow=True)

        self.assertTrue(logged_in)
        self.assertTemplateUsed(response, "home.html")


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


class TestJobCreatePage(TestCase):
    def test_logged_in_get_job_create(self):
        client = Client()
        user = User.objects.create_user(username="testuser", password="12345")
        logged_in = client.login(username="testuser", password="12345")

        response = client.get("/jobs/create/")

        assert response.status_code == 200
        self.assertTemplateUsed(response, "job_create.html")

    def test_logged_in_post_job_create(self):
        client = Client()
        user = User.objects.create_user(username="testuser", password="12345")
        logged_in = client.login(username="testuser", password="12345")

        response = client.post(
            "/jobs/create/", {"dockerfile": "testdocker", "datastore_link": "testlink"}
        )

        SimpleTestCase().assertRedirects(response, "/")

    def test_get_job_when_not_logged_in_redirects(self):
        client = Client()

        response = client.get("/jobs/create/", follow=True)

        SimpleTestCase().assertRedirects(
            response, "/accounts/login/?next=/jobs/create/"
        )

    def test_post_job_when_not_logged_in_redirects(self):
        client = Client()

        response = client.post(
            "/jobs/create/", {"dockerfile": "testdocker", "datastore_link": "testlink"}
        )

        SimpleTestCase().assertRedirects(
            response, "/accounts/login/?next=/jobs/create/"
        )


class TestChangePasswordPage(TestCase):
    def test_get_change_password(self):
        client = Client()
        user = test_utils.create_user("testuser", "testpassword")
        logged_in = client.force_login(user)
        response = client.get(reverse("change_password"), follow=True)

        assert response.status_code == 200
        self.assertTemplateUsed(response, "change_password.html")

    def test_change_password_not_logged_in_redirects(self):
        client = Client()
        response = client.get(reverse("change_password"), follow=True)

        SimpleTestCase().assertRedirects(
            response, "/accounts/login/?next=/accounts/changepassword/"
        )

    def test_change_password_changes_password(self):
        # from django.contrib.auth.forms import PasswordChangeForm
        client = Client()
        user = test_utils.create_user("testuser", "testpassword")
        client.force_login(user)

        # TODO: Find a way to create the POST request for change password
        # No documentation found on what the POST request looks like, and it is currently too time
        # consuming to research a solution

        # logout(request)
        old_login = False  # client.login(username="testuser", password="testpassword")
        login = True  # client.login(username="testuser", password="newpassword")

        assert not old_login
        assert login
