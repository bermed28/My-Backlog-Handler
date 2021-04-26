import datetime

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect("homepage")

    else:
        form = RegisterForm(request.POST)
        return render(request, "register/register.html", {"form": form})


# def register(response):
#     if response.user.is_authenticated:
#         return redirect("homepage")
#
#     else:
#         if response.method == "POST":
#             form = RegisterForm(response.POST)
#             if form.is_valid():
#                 form.save()
#             return redirect("homepage")
#         else:
#             form = RegisterForm()
#
#         return render(response, "register/register.html", {"form": form})


