from django.forms import ModelForm

from .models import Job


class JobCreateForm(ModelForm):
    class Meta:
        model = Job
        fields = ["finished", "time_started", "dockerfile", "datastore_link"]
