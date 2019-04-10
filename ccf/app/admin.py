from app.models import FinishedJob, Job
from django.contrib import admin

# Allow the Django admin to manage the Jobs database.
admin.site.register(Job)
admin.site.register(FinishedJob)
