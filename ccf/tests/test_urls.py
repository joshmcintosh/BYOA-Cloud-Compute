from unittest.mock import Mock, patch

import pytest
import test_utils
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


class TestJobsPage(TestCase):
    def test_logged_in_get_jobs(self):
        client = Client()
        user = User.objects.create_user(username="testuser", password="12345")
        logged_in = client.login(username="testuser", password="12345")

        response = client.get("/jobs/")

        assert response.status_code == 200
        self.assertTemplateUsed(response, "jobs.html")

    def test_get_jobs_when_not_logged_in_redirects(self):
        client = Client()

        response = client.get("/jobs/", follow=True)

        SimpleTestCase().assertRedirects(response, "/accounts/login/?next=/jobs/")

    @pytest.mark.django_db()
    def test_job_lists_are_correct(self):
        client = Client()
        test_user = test_utils.create_user("test_user", "test_password")
        logged_in = client.force_login(test_user)
        job = test_utils.create_job(test_user, "some_docker", "some_link")
        job = test_utils.create_job(
            test_user, "other_docker", "other_link", finished=True
        )

        response = client.get("/jobs/")
        uj = response.context["unfinished_jobs"][0]
        fj = response.context["finished_jobs"][0]

        print(uj.dockerfile, uj.dockerfile == ("some_docker", "some_link"))

        assert (uj.dockerfile, uj.datastore_link, uj.finished) == (
            "some_docker",
            "some_link",
            False,
        )
        assert (fj.dockerfile, fj.datastore_link, fj.finished) == (
            "other_docker",
            "other_link",
            True,
        )
