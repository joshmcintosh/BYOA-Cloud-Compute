from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
@login_required
def homepage_view(request):
    return render(request, "tmp_home.html")
