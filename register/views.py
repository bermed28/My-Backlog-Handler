import datetime

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings


# Create your views here.
def register(response):
    if response.user.is_authenticated:
        return redirect("homepage")
    else:
        if response.method == "POST":
            form = RegisterForm(response.POST)
            if form.is_valid():
                form.save()
            return redirect("homepage")
        else:
            form = RegisterForm()

        return render(response, "register/register.html", {"form": form})


def process_request(self, request):
    if request.user.is_authenticated():
        current_datetime = datetime.datetime.now()
        if 'last_login' in request.session:
            last = (current_datetime - request.session['last_login']).seconds
            if last > settings.SESSION_IDLE_TIMEOUT:
                logout(request, '/')
        else:
            request.session['last_login'] = current_datetime
    return None
