from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('register/', views.registration, name="register"),
    path('about-us/', views.aboutUs, name="about-us"),
    path('backlog/', views.backlog, name="backlog"),
    path('game-article-template/', views.gameArticleTemplate, name="game-article-template"),
    path('library/', views.library, name="library"),
    path('api', include(router.urls)),
    path('/api-auth/', include('rest_framework.urls', namespace="rest framework")),
    path('login/', views.login, name="login"),
]
