from django.shortcuts import redirect


# Create your views here.
def homepage_view(request):
    return redirect("/accounts/login/")
