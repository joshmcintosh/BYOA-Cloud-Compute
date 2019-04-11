import base64
import importlib
import os
import shutil
import subprocess
from multiprocessing.pool import ThreadPool

from app.data_fetch import divide_list, get_STAC_items_from_catalog
from app.forms import JobCreateForm
from app.models import FinishedJob, Job
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.views import generic

### TODO: Cleanup this file.
# This file was made an absolute nightmare due to a deadline, so sacrifices to
# both code quality and functionality are made.
# As of right now, the entire functionality for running a user's code needs to
# be re-written to be more safe.


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

        # TODO: get link to catalog and dockerfile
        config = form.cleaned_data["config"]
        catalog = form.cleaned_data["catalog_link"]

        print(f"New job requested with\n\tconfig: {config}\n\tcatalog_link: {catalog}")
        # config = "NAME Ethan; GIT_CLONE  https://github.com/eetar1/Seng371-Worker; INSTALL_REQUIREMENTS; PYTHON_RUN dataFetch.py"
        # catalog = (
        #    "https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/065/094/catalog.json"
        # )

        commands = lex_config(config, job.jobNum)
        name = commands[0]
        commands = commands[1:]

        run_setup(commands, name)

        # This is a little hack. Sorry.
        # Create an event pool to spawn a thread to start working on their job.
        # As this is a prototype system, gloss over the
        # complex stuff of figuring out how many processes there should be.
        # Assuming 5 is good. TODO: do this better.
        patitions = 2
        timeout = 50
        items = get_STAC_items_from_catalog(catalog)
        divided_items = divide_list(items, patitions)

        event_pool = ThreadPool(processes=patitions)
        callbacks = []
        for i in range(patitions):
            callbacks.append(
                event_pool.apply_async(
                    start_job, (commands[-1], divided_items[i], name, i)
                )
            )
        outDir = watch_callbacks(callbacks, timeout)
        storeImages(outDir + "/outputs", job)

        shutil.rmtree(outDir)
        job.finished = True
        job.save()

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
def job_images_view(request, jobNum):
    images = FinishedJob.objects.filter(jobNum=jobNum)
    context = {"jobNum": jobNum, "images": images}
    return render(request, "job_images.html", context)


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


def start_job(command_string: str, data_links: list, name: str, thread_number: int):
    """ Start running each job.

        The script being called *must* contain a "run_process" method.
        This method will return whatever needs to be stored as the return for
        that run.

        The run process method must accept all args *in order* of how they are called
        from the config file. The last arg accepted by run_process *must* be the
        datastore link.
    """

    for data_index, data_link in enumerate(data_links):
        execute_command = (
            command_string
            + f" {data_link}"
            + f" outputs/{name}.thread{thread_number}.item{data_index}"
        )
        print(f"running: {execute_command} with {execute_command.split(' ')}")
        subprocess.call(execute_command.split(" "), cwd=f".process/{name}/")

    # clean up... ie make the caller cleanup.
    return f".process/{name}"


def lex_config(config: str, jobNum: int):
    """ Processes a config file and returns the commands that need to be run.

        This project has only *very* basic support. The allowed commands are
        NAME [Name of process]
        GIT_CLONE [git repo to clone]
        INSTALL_REQUIREMENTS
        PYTHON_RUN [python script to run] [script args]

        Any line in the config not matching one of these commands will be ignored.
        Any arguments following the final arguments in the command will be ignored.

        A config MUST start with a NAME command, and end with a python command.

        The GIT_CLONE command MUST use the HTTPS not SSH.

    """

    config_commands = config.split(";")
    commands = []
    name = str(jobNum) + "." + config_commands[0].replace("NAME ", "").strip()
    config_commands = config_commands[1:]
    commands.append(name)

    for config_command in config_commands:

        config_tokens = config_command.split()

        if config_tokens[0] == "GIT_CLONE":
            commands.append(f"git clone {config_tokens[1]} .process/{name} -q")
        elif config_tokens[0] == "INSTALL_REQUIREMENTS":
            commands.append(f"pip install -r .process/{name}/requirements.txt")
        elif config_tokens[0] == "PYTHON_RUN":
            commands.append(f"python {' '.join(config_tokens[1:])}")
            # commands.append(f"{' '.join(config_tokens[1:])}")

    return commands


def watch_callbacks(callbacks, timeout):
    results = []
    for callback in callbacks:
        results.append(callback.get(timeout))
    if len(results) < 1:
        return None
    return results[0]


def storeImages(outDir, Parentjob):
    job = FinishedJob()
    for entry in os.listdir(outDir):
        job = FinishedJob()
        job.jobNum = Parentjob.jobNum
        enco = ""
        with open(outDir + "/" + entry, "rb") as fp:
            enco = base64.b64encode(fp.read())
        job.image = str(enco)[2:-1]
        job.save()


def run_setup(commands, name):
    if not os.path.exists(f".process/{name}/.git"):
        for command in commands[:-1]:
            # TODO: FIx everything about this.
            print(f"running: {command} with {command.split(' ')}")
            subprocess.run(command.split(" "))
        try:
            os.makedirs(f".process/{name}/outputs")
        except:
            pass


class SignUp(generic.CreateView):
    """Sign-up Page

    Returns to the user the sign-up template.
    """

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"
