from app.models import Job
from django.contrib.auth.models import User


def create_user(username, password):
    test_user = User.objects.create_user(username)
    test_user.set_password(password)
    test_user.save()
    return test_user


def create_job(test_user, config, catalog_link, finished=False):
    job = Job(
        finished=finished, config=config, catalog_link=catalog_link, user=test_user
    )
    job.save()
    return job
