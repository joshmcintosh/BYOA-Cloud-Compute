import django
import pytest
from app.models import Job


@pytest.mark.django_db()
def test_create_job_entry():
    job = Job(
        finished=False,
        dockerfile="this is a dockerfile.",
        datastore_link="abc.com",
        user_id="123",
    )

    job.save()

    assert len(Job.objects.all()) == 1


@pytest.mark.django_db()
def test_creating_job_without_dockerfile_raises_integrity_error():
    job = Job(finished=False, datastore_link="abc.com", user_id="123")

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()


@pytest.mark.django_db()
def test_create_job_without_datastore_link_raises_integrity_error():
    job = Job(finished=False, dockerfile="this is a dockerfile.", user_id="123")

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()


@pytest.mark.django_db()
def test_create_job_without_finished_auto_fills_field_to_false():
    job = Job(
        dockerfile="This is a dockerfile", datastore_link="abc.com", user_id="123"
    )

    assert not job.finished


@pytest.mark.django_db()
def test_create_job_without_user_raises_integrity_error():
    job = Job(
        finished=False, dockerfile="this is a dockerfile.", datastore_link="abc.com"
    )

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()


@pytest.mark.django_db()
def test_create_job_with_user_equal_zero_raises_integrity_error():
    job = Job(
        finished=False,
        dockerfile="this is a dockerfile.",
        datastore_link="abc.com",
        user_id=0,
    )

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()
