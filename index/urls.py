from django.urls import include, path
from rest_framework import routers
from . import views
from .views import LibraryInsertion


from register import views as v
router = routers.DefaultRouter()
router.register(r'users', views.PlayerAccountViewSet)
# app_name = 'index'
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.HomeGameView.as_view(), name="homepage"),
    path('about-us/', views.aboutUs, name="about-us"),
    path('backlog/my-backlog/', views.BacklogGameView.as_view(), name="backlog"),
    path(r'^(?P<game_id>\w+)/$', views.gameArticleTemplate, name="game-article-template"),
    #url(r'(?P<first_name>\w+)_(?P<last_name>\w+)/$', view_name, name='url_name')
    # {% url 'urlname' user.firstname user.lastname %}

    path('library/', views.LibraryGameView.as_view(), name="library"),
    path( r'library/add/^(?P<game_id>\w+)/$', LibraryInsertion.as_view(), name="library-add"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace="rest framework")),

    path('backlog/tips-tricks/', views.tips, name="tips-tricks"),
    path('games/', views.GamesView.as_view(), name="games"),
    path('games/new-releases/', views.newReleases, name="new-releases"),
    path('games/popular/', views.popGames, name="popGames"),
    path('games/upcoming/', views.upGames, name="upGames"),
    path('search/', views.SearchResultsGameView.as_view(), name='search_results'),
    path('user/profile/', views.profile, name='profile'),
    path('user/favorites/', views.favorites, name='favorites'),
    path('user/wishlist/', views.wishlist, name='wishlist'),
    path('user/settings/', views.settings, name='settings'),
    path('404/', views.fourOFour, name='404'),
    path('500/', views.fiveHundred, name='500'),
    path('403/', views.fourOThree, name='403'),
    path('400/', views.fourHundred, name='400'),
    path('blankQuery/', views.blankQuery, name='blankQuery'),
]

