from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views import generic

from .forms import JobCreateForm


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("change_password")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})


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
        return HttpResponseRedirect(reverse("home"))
    else:
        form = JobCreateForm()

    context = {"form": form}

    return render(request, "job_create.html", context)


class SignUp(generic.CreateView):
    """Sign-up Page

    Returns to the user the sign-up template.
    """

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"
