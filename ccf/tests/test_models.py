import django
import pytest
import test_utils
from app.models import Job


@pytest.mark.django_db()
def test_create_job_entry():
    test_user = test_utils.create_user("test user", "test_password")
    job = Job(
        finished=False,
        config="this is a config.",
        catalog_link="abc.com",
        user=test_user,
    )

    job.save()

    assert len(Job.objects.all()) == 1


@pytest.mark.django_db()
def test_creating_job_without_config_raises_integrity_error():
    test_user = test_utils.create_user("test user", "test_password")
    job = Job(finished=False, catalog_link="abc.com", user=test_user)

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()


@pytest.mark.django_db()
def test_create_job_without_catalog_link_raises_integrity_error():
    test_user = test_utils.create_user("test user", "test_password")
    job = Job(finished=False, config="this is a config.", user=test_user)

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()


@pytest.mark.django_db()
def test_create_job_without_finished_auto_fills_field_to_false():
    test_user = test_utils.create_user("test user", "test_password")
    job = Job(config="This is a config", catalog_link="abc.com", user=test_user)

    assert not job.finished


@pytest.mark.django_db()
def test_create_job_without_user_raises_integrity_error():
    test_user = test_utils.create_user("test user", "test_password")
    job = Job(finished=False, config="this is a config.", catalog_link="abc.com")

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()
