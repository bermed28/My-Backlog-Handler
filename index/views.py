from django.shortcuts import render, redirect
# Create your views here.
from rest_framework import viewsets
from django.views.generic import ListView
from django.db.models import Q

from .serializers import GameModelSerializer, ImageModelSerializer, DeveloperModelSerializer, GenreModelSerializer, \
PlayerAccountSerializer,LibraryModelSerializer, LibraryMembershipSerializer

from .models import Game_Model, PlayerAccount, Image_Model, Developer_Model, Genre_Model, Library_Model, Library_Membership

"""VIEWSETS"""
class PlayerAccountViewSet(viewsets.ModelViewSet):
    queryset = PlayerAccount.objects.all().order_by('player_name')
    serializer_class = PlayerAccountSerializer

class GameModelViewSet(viewsets.ModelViewSet):
    queryset = Game_Model.objects.all().order_by('game_id')
    serializer_class = GameModelSerializer

class ImageModelViewSet(viewsets.ModelViewSet):
    queryset = Image_Model.objects.all().order_by('img_id')
    serializer_class = ImageModelSerializer

class DeveloperModelViewSet(viewsets.ModelViewSet):
    queryset = Developer_Model.objects.all().order_by('dev_id')
    serializer_class = DeveloperModelSerializer

class GenreModelViewSet(viewsets.ModelViewSet):
    queryset = Genre_Model.objects.all().order_by('genre_id')
    serializer_class = GenreModelSerializer

class LibraryModelViewSet(viewsets.ModelViewSet):
    queryset = Library_Model.objects.all().order_by('owner_id')
    serializer_class = LibraryModelSerializer

class LibraryMembershipViewSet(viewsets.ModelViewSet):
    queryset = Library_Membership.objects.all().order_by('library')
    serializer_class = LibraryMembershipSerializer


"""REDIRECTS"""
def homepage(request):
    """
    Uncomment to test login and logout
    if request.user.is_authenticated:
        print("Logged In")
    else:
        print("Logged Out")
    """
    return render(request,"home/homepage.html")

class SearchResultsView(ListView):
    model = Game_Model
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Game_Model.objects.filter(
            Q(game_title__icontains=query)
        )
        return object_list

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

def newReleases(request):
    return render(request, 'home/new-releases.html')

def popGames(request):
    return render(request, 'home/popular-games.html')

def upGames(request):
    return render(request, 'home/upcoming-games.html')







