from django.shortcuts import render, redirect
# Create your views here.
from rest_framework import viewsets

from .serializers import PlayerAccountSerializer
from .models import PlayerAccount

class PlayerAccountViewSet(viewsets.ModelViewSet):
    queryset = PlayerAccount.objects.all().order_by('player_name')
    serializer_class = PlayerAccountSerializer

def homepage(request):
    return render(request,"home/homepage.html")

def registration(request):
    return render(request, 'home/registration.html')

def aboutUs(request):
    return render(request, 'home/about-us.html')

def backlog(request):
    return render(request, 'home/backlog.html')

def gameArticleTemplate(request):
    return render(request, 'home/game-article-template.html')

def library(request):
    return render(request, 'home/library.html')

def tips(request):
    return render(request, 'home/tips.html')







