import django
from django.contrib.auth.models import User
from django.db import models
from django.db.utils import IntegrityError


class Job(models.Model):
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

        super(Job, self).save(*args, **kwargs)
