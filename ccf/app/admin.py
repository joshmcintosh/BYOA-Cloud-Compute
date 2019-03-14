from app.models import Jobs
from django.contrib import admin

# Allow the Django admin to manage the Jobs database.
admin.site.register(Jobs)
