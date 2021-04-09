"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import handler404, handler500, handler403, handler400
from django.urls import path, include
from register import views as v

urlpatterns = [
    path('', include('index.urls')),
    path('admin/', admin.site.urls),
    path('register/', v.register, name="register"),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('django.contrib.auth.urls'))
]

handler404 = 'index.views.fourOFour'
handler500 = 'index.views.fiveHundred'
handler403 = 'index.views.fourOThree'
handler400 = 'index.views.fourHundred'
