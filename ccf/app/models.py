import django
from django.contrib.auth.models import User
from django.db import models
from django.db.utils import IntegrityError


class Job(models.Model):
    jobNum = models.AutoField(primary_key=True, default=1)
    finished = models.BooleanField(default=False)
    time_started = models.DateTimeField(default=django.utils.timezone.now, blank=False)
    dockerfile = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Arbitrary max length for prototype.
    datastore_link = models.CharField(max_length=50)

    def save(self, *args, **kwargs):

        if not self.dockerfile:
            raise IntegrityError("dockerfile value must not be blank.")

        if not self.datastore_link:
            raise IntegrityError("datastore_link value must not be blank.")

        # Gross hack to convert an error with app.models.Job.user.RelatedObjectDoesNotExist
        # to an integrity error. We prefer an integriy error here as a job without a
        # user is an invalid state.
        try:
            _ = self.user
        except Job.user.RelatedObjectDoesNotExist:
            raise IntegrityError("user could not be found.")

        super(Job, self).save(*args, **kwargs)


class FinishedJob(models.Model):

    jobNum = models.IntegerField(default=0)
    image = models.ImageField(upload_to="/")

    def save(self, *args, **kwargs):
        super(FinishedJob, self).save(*args, **kwargs)
