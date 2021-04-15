from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from rest_framework import viewsets
from django.views.generic import ListView, RedirectView
from django.db.models import Q
from igdb.wrapper import IGDBWrapper
from .request import getSummary
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

class HomeGameView(ListView):
    model = Game_Model
    template_name = '../templates/home/homepage.html'

    def get_list(self):
        game_model_list = Game_Model.objects
        return game_model_list

class LibraryGameView(ListView):
    paginate_by = 15
    model = Game_Model
    template_name = '../templates/home/library.html'

    def get_list(self):
        game_model_list = Game_Model.objects
        return game_model_list

class BacklogGameView(ListView):
    paginate_by = 15
    model = Game_Model
    template_name = '../templates/home/backlog.html'

    def get_list(self):
        game_model_list = Game_Model.objects
        return game_model_list


class SearchResultsGameView(ListView):
    paginate_by = 15
    model = Game_Model
    template_name = '../templates/home/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        game_model_list = Game_Model.objects.filter(
            Q(game_title__icontains=query)
        )
        return game_model_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

class SearchResultsImgView(ListView):
    paginate_by = 15
    model = Image_Model
    template_name = '../templates/home/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        image_model_ist = Image_Model.objects.filter(
            Q(game_title__icontains=query)
        )
        return image_model_ist

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

def registration(request):
    return render(request, 'home/registration.html')

def aboutUs(request):
    return render(request, 'home/about-us.html')

def gameArticleTemplate(request, game_id):
    wrapper = IGDBWrapper("2zu4l0leu7rrc9i8ysagqlxuu5rh89", "r2raogtcmwho8ja4fv6b8si2h7u7ag")
    gameArticle = Game_Model.objects.get(game_id=game_id)
    summary = getSummary(game_id,wrapper)
    return render(request, 'home/game-article-template.html', {'gameArticle' : gameArticle, "gameSummary": summary})


def tips(request):
    return render(request, 'home/tips.html')

def gamesSection(request):
    return render(request, 'home/games.html')

def newReleases(request):
    return render(request, 'home/new-releases.html')

def popGames(request):
    return render(request, 'home/popular-games.html')

def upGames(request):
    return render(request, 'home/upcoming-games.html')

def settings(request):
    return render(request, 'home/settings.html')

def wishlist(request):
    return render(request, 'home/wishlist.html')

def profile(request):
    return render(request, 'home/profile.html')

def favorites(request):
    return render(request, 'home/favorites.html')

def fourOFour(request, exception):
    return render(request=request, template_name='home/errorHandling/404.html')

def fiveHundred(request):
    return render(request=request, template_name='home/errorHandling/500.html')

def fourHundred(request, exception):
    return render(request=request, template_name='home/errorHandling/400.html')

def fourOThree(request, exception):
    return render(request=request, template_name='home/errorHandling/403.html')

def blankQuery(request):
    return render(request=request, template_name='home/errorHandling/blankQuery.html')





