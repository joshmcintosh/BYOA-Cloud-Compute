from django.forms import ModelForm

from .models import Job


class JobCreateForm(ModelForm):
    class Meta:
        model = Job
        fields = ["config", "catalog_link"]
