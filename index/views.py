
# Create your views here.

from rest_framework import viewsets
from django.views.generic import ListView
from igdb.wrapper import IGDBWrapper
from .request import getSummary
from .serializers import GameModelSerializer, ImageModelSerializer, LibraryModelSerializer, LibraryMembershipSerializer, RatingModelSerializer, PlayerAccountSerializer

from .models import Ratings_Model

from .forms import LibraryAddForm, ProfilePersonalization
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date, timedelta
from .models import Game_Model, PlayerAccount, Image_Model, Library_Model, Library_Membership
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from db_connection_tester import queryDo

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

class LibraryDelete(View):
    def get(self, request, game_id, **kwargs):
        player_library = Library_Model.objects.filter(
            owner_id=self.request.user.id
        )
        print(player_library)
        game = Library_Membership.objects.filter(library=player_library[0], game=game_id)
        print(game)
        game.delete()
        return HttpResponseRedirect(reverse("library"))



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

def checkLibraryForGame(user_id, game_id):
    player_library = Library_Model.objects.filter(
        owner_id=user_id
    )
    game = player_library[0].games.filter(game_id=game_id)
    game_available = True if game.count() == 0 else False
    return game_available


class LibraryGameView(ListView):
    model = Library_Membership
    paginate_by = 15
    template_name = '../templates/home/library.html'

    def get_queryset(self):
        # query = self.request.GET.get('q')

        player_library = Library_Model.objects.filter(
            owner_id=self.request.user.id
        )
        if player_library.exists():
            library_games = Library_Membership.objects.filter(library=player_library[0])
            print(library_games)
        else:
            new_Library = Library_Model(owner_id=self.request.user)
            new_Library.save()
            library_games = Library_Membership.objects.filter(library=new_Library)
            return []



        return library_games


class BacklogGameView(ListView):
    paginate_by = 15
    model = Library_Membership
    template_name = '../templates/home/backlog.html'

    def get_queryset(self):
        player_library = Library_Model.objects.filter(owner_id=self.request.user.id)

        if player_library.exists():
            startdate = date.today()
            enddate = startdate + timedelta(days=-60)
            # Sample.objects.filter(date__range=[startdate, enddate])
            library = Library_Membership.objects.filter(library=player_library[0])
            backlog = (library.filter(last_played__lt=enddate) | library.filter(forcedToBacklog=True)).distinct()
            print(backlog)
        else:
            new_Library = Library_Model(owner_id=self.request.user)
            new_Library.save()
            library_games = Library_Membership.objects.filter(library=new_Library)
            return []

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

    if request.method == 'POST' and request.POST.get('overall_rating'):
        if request.user.is_authenticated:
            saveRating = Ratings_Model(user_id_id=request.user.id, game_id=game_id,
                                       overall_rating=request.POST.get('overall_rating'))
            saveRating.save()
            messages.success(request, 'Rating Saved Successfully!')
            return render(request, 'home/game-article-template.html',
                          {'gameArticle': gameArticle, "gameSummary": summary})
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
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


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            messages.error(request, 'Please enter your correct password.')
            return redirect('password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'home/password.html', {
            'form': form
        })

def customizeProfile(request):
    if request.method == 'POST':
        form = ProfilePersonalization(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your account was successfully updated!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error below.')
            return redirect('settings')
    else:
        form = ProfilePersonalization(instance=request.user)
        return render(request, 'home/settings.html', {
            'form': form
        })

def deleteUser(request):
    if request.GET.get('delete'):
        queryDo(f'DELETE FROM public.auth_user WHERE id={request.user.id}')
        print("User deleted")
        return redirect('homepage')

    return render(request, 'home/deleteAccount.html')