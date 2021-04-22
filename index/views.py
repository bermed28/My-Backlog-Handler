from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from rest_framework import viewsets
from django.views.generic import ListView, RedirectView
from django.db.models import Q
from django.contrib import messages
from igdb.wrapper import IGDBWrapper
from .request import getSummary
from .serializers import GameModelSerializer, ImageModelSerializer, DeveloperModelSerializer, GenreModelSerializer, \
    LibraryModelSerializer, LibraryMembershipSerializer, RatingModelSerializer, PlayerAccountSerializer

from .models import Game_Model, PlayerAccount, Image_Model, Developer_Model, Genre_Model, Library_Model, \
    Library_Membership, Ratings_Model

from .forms import LibraryAddForm
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from datetime import date, timedelta
from .models import Game_Model, PlayerAccount, Image_Model, Developer_Model, Genre_Model, Library_Model, \
    Library_Membership
from django.db.models import Q

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


class RatingModelViewSet(viewsets.ModelViewSet):
    queryset = Ratings_Model.objects.all().order_by('overall_rating')
    serializer_class = RatingModelSerializer


"""REDIRECTS"""


class HomeGameView(ListView):
    model = Game_Model
    template_name = '../templates/home/homepage.html'

    def get_list(self):
        game_model_list = Game_Model.objects
        return game_model_list


# //////////////////////////////////////////////////////////////////////

"""
Checks if game is player's library and if it is it return False else return True
"""


def checkLibraryForGame(user_id, game_id):
    player_library = Library_Model.objects.filter(
        owner_id=user_id
    )
    game = player_library[0].games.filter(game_id=game_id)
    game_available = True if game.count() == 0 else False
    return game_available


class LibraryInsertion(View):

    def get(self, request, game_id, **kwargs):
        form = LibraryAddForm()
        gameArticle = Game_Model.objects.get(game_id=game_id)
        game_available = checkLibraryForGame(self.request.user.id, game_id)

        context = {
            "game_form": form,
            "gameArticle": gameArticle,
            "game_available": game_available
        }

        return render(request, 'home/library-add.html', context)

    def post(self, request, game_id, **kwargs):
        form = LibraryAddForm(request.POST or None)
        gameArticle = Game_Model.objects.get(game_id=game_id)
        if form.is_valid():
            player_library, created = Library_Model.objects.get_or_create(owner_id=request.user)

            membership = Library_Membership(
                game=gameArticle,
                library=player_library,
                last_played=form.cleaned_data['last_played'],
                is_finished=form.cleaned_data['is_finished'],
            )
            membership.save()

            print("game_id", game_id)
            print("last_played = ", form.cleaned_data['last_played'])
            print("is_finished = ", form.cleaned_data['is_finished'])
            form = LibraryAddForm()
        else:
            print(form.errors)
        return HttpResponseRedirect(reverse("library"))


# def LibraryInsertion(request, game_id):
#     form = LibraryAddForm(request.POST or None)
#     gameArticle = Game_Model.objects.get(game_id=game_id)
#     if request.method == "POST":
#         print("user = ",  request.user)
#         if form.is_valid():
#             player_library, created = Library_Model.objects.get_or_create(owner_id=request.user)
#
#             membership = Library_Membership(
#             game = gameArticle,
#             library = player_library,
#             last_played = form.cleaned_data['last_played'],
#             is_finished =form.cleaned_data['is_finished'],
#             )
#             membership.save()
#
#             print("game_id", game_id)
#             print("last_played = ",form.cleaned_data['last_played'])
#             print("is_finished = ", form.cleaned_data['is_finished'])
#             form = LibraryAddForm()
#         else:
#             print(form.errors)
#         return redirect(request.path)
#     print(Library_Model.objects.all())
#
#     # form = LibraryAddForm(request.POST or None)
#     # gameArticle = Game_Model.objects.get(game_id=game_id)
#     context = {
#         "game_form":form,
#         "gameArticle":gameArticle
#     }
#
#     return render(request, 'home/library-add.html', context)


class LibraryGameView(ListView):
    model = Library_Membership
    paginate_by = 15
    template_name = '../templates/home/library.html'

    def get_queryset(self):
        # query = self.request.GET.get('q')

        player_library = Library_Model.objects.filter(
            owner_id=self.request.user.id
        )

        library_games = Library_Membership.objects.filter(library=player_library[0])
        print(library_games)

        return library_games


class BacklogGameView(ListView):
    paginate_by = 15
    model = Library_Membership
    template_name = '../templates/home/backlog.html'

    def get_queryset(self):
        player_library = Library_Model.objects.filter(
            owner_id=self.request.user.id
        )

        startdate = date.today()
        enddate = startdate + timedelta(days=-60)
        # Sample.objects.filter(date__range=[startdate, enddate])
        backlog = Library_Membership.objects.filter(library=player_library[0]).filter(last_played__lt=enddate)
        print(backlog)
        return backlog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


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


class GamesView(ListView):
    paginate_by = 15
    model = Game_Model
    template_name = '../templates/home/games.html'

    def get_list(self):
        game_model_list = Game_Model.objects
        return game_model_list

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
    summary = getSummary(game_id, wrapper)
    if request.user.is_authenticated:
        if request.method == 'POST' and request.POST.get('overall_rating'):
            saveRating = Ratings_Model(user_id_id=request.user.id, game_id=game_id,
                                       overall_rating=request.POST.get('overall_rating'))
            saveRating.save()
            messages.success(request, 'Rating Saved Successfully!')
            return render(request, 'home/game-article-template.html',
                          {'gameArticle': gameArticle, "gameSummary": summary})
        else:
            return render(request, 'home/game-article-template.html',
                          {'gameArticle': gameArticle, "gameSummary": summary})
    else:
        messages.error(request, 'Log In To Have Access To Our Rating System')
        return render(request, 'home/game-article-template.html',
                      {'gameArticle': gameArticle, "gameSummary": summary})


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
