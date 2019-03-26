from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import Job


@login_required
def homepage_view(request):
    """Homepage to Login Redirect

    Returns to the user the homepage template if they are logged in, otherwise redirects them
    to the login page.
    """
    return render(request, "tmp_home.html")


@login_required
def jobs_view(request):
    """Jobs Page

    Returns to the user all of their jobs and their status.
    """
    jobs_list = Job.objects.filter(user=request.user)
    context = {"jobs_list": jobs_list}
    return render(request, "jobs.html", context)


class SignUp(generic.CreateView):
    """Sign-up Page

    Returns to the user the sign-up template.
    """

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"
