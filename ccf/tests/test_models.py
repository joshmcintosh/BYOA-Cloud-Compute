import django
import pytest
from app.models import Jobs


@pytest.mark.django_db()
def test_create_job_entry():
    job = Jobs(
        finished=False, dockerfile="this is a dockerfile.", datastore_link="abc.com"
    )

    job.save()

    assert len(Jobs.objects.all()) == 1


@pytest.mark.django_db()
def test_creating_job_without_dockerfile_raises_integrity_error():
    job = Jobs(finished=False, datastore_link="abc.com")

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()


@pytest.mark.django_db()
def test_create_job_without_datastore_link_raises_integrity_error():
    job = Jobs(finished=False, dockerfile="this is a dockerfile.")

    with pytest.raises(django.db.utils.IntegrityError):
        job.save()


@pytest.mark.django_db()
def test_create_job_without_finished_auto_fills_field_to_false():
    job = Jobs(dockerfile="This is a dockerfile", datastore_link="abc.com")

    assert not job.finished
