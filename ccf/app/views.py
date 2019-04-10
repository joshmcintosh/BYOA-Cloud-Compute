from multiprocessing.pool import ThreadPool

from app.data_fetch import divide_list, get_STAC_items_from_catalog
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

        #TODO: get link to catalog and dockerfile
        catalog = ""
        config = "https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/065/094/catalog.json"

        # This is a little hack. Sorry.
        # Create an event pool to spawn a thread to start working on their job.
        # As this is a prototype system, gloss over the
        # complex stuff of figuring out how many processes there should be.
        # Assuming 5 is good. TODO: do this better.
        patitions = 2;
        timeout = 50;
        items = get_STAC_items_from_catalog(catalog)
        divided_items = divide_list(items, patitions)

        event_pool = ThreadPool(processes=2)
        callbacks = []
        for i in range(patitions):
            callbacks.append(event_pool.apply_async(start_job(), (config, divided_items[i])))
        watch_callbacks(callbacks, timeout)


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


def watch_callbacks(callbacks, timeout):
    results = []
    for callback in callbacks:
        results.append(callback.get(timeout))
    return results

class SignUp(generic.CreateView):
    """Sign-up Page

    Returns to the user the sign-up template.
    """

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


