from multiprocessing.pool import ThreadPool

from app.forms import JobCreateForm
from app.models import Job
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views import generic


def homepage_view(request):
    """Homepage to Login Redirect

    Returns to the user the homepage template if they are logged in, otherwise redirects them
    to the login page.
    """
    return render(request, "home.html")


@login_required
def job_create_view(request):
    """Job Create Page

    Returns to the user the job create page. The user must be logged in.
    """
    if request.method == "POST":
        form = JobCreateForm(request.POST)
        job = form.save(commit=False)
        job.user = request.user
        job.save()

        # This is a little hack. Sorry.
        # Create an event pool to spawn a thread to start working on their job.
        # As this is a prototype system, gloss over the
        # complex stuff of figuring out how many processes there should be.
        # Assuming 5 is good. TODO: do this better.
        event_pool = ThreadPool(processes=5)

        return HttpResponseRedirect(reverse("jobs"))
    else:
        form = JobCreateForm()

    context = {"form": form}

    return render(request, "job_create.html", context)


@login_required
def jobs_view(request):
    """Jobs Page

    Returns to the user all of their jobs and their status.
    """
    unfinished_jobs = Job.objects.filter(user=request.user).filter(finished=False)
    finished_jobs = Job.objects.filter(user=request.user).filter(finished=True)
    context = {"unfinished_jobs": unfinished_jobs, "finished_jobs": finished_jobs}
    return render(request, "jobs.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("home")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})


def start_job(config):
    pass


class SignUp(generic.CreateView):
    """Sign-up Page

    Returns to the user the sign-up template.
    """

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"
