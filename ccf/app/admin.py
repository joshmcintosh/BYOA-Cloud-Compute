from app.models import Job
from django.contrib import admin

# Allow the Django admin to manage the Jobs database.
admin.site.register(Job)
