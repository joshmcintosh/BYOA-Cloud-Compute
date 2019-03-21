import django
import pytest
from app.models import Job


@pytest.fixture
@pytest.mark.django_db()
def test_user():
    from django.contrib.auth.models import User

    test_user = User.objects.create_user(
        "john", "lennon@thebeatles.com", "johnpassword"
    )
    test_user.save()
    return test_user


@pytest.mark.django_db()
def test_create_job_entry(test_user):
    job = Job(
        finished=False,
        dockerfile="this is a dockerfile.",
        datastore_link="abc.com",
        user=test_user,
    )

    job.save()

    assert len(Job.objects.all()) == 1


@pytest.mark.django_db()
def test_creating_job_without_dockerfile_raises_integrity_error(test_user):
    job = Job(finished=False, datastore_link="abc.com", user=test_user)

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()


@pytest.mark.django_db()
def test_create_job_without_datastore_link_raises_integrity_error(test_user):
    job = Job(finished=False, dockerfile="this is a dockerfile.", user=test_user)

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()


@pytest.mark.django_db()
def test_create_job_without_finished_auto_fills_field_to_false(test_user):
    job = Job(
        dockerfile="This is a dockerfile", datastore_link="abc.com", user=test_user
    )

    assert not job.finished


@pytest.mark.django_db()
def test_create_job_without_user_raises_integrity_error(test_user):
    job = Job(
        finished=False, dockerfile="this is a dockerfile.", datastore_link="abc.com"
    )

    with pytest.raises(Job.user.RelatedObjectDoesNotExist):
        job.save()
