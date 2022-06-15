"""app_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from app_api.views import register_user, login_user
from rest_framework import routers
from django.conf.urls import include

from app_api.views.Artist import ArtistView
from app_api.views.Genre import GenreView
from app_api.views.Gig import GigView
from app_api.views.Instrument import InstrumentView
from app_api.views.Musician import MusicianView
from app_api.views.Skill_Level import SkillLevelView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'artists', ArtistView, 'artist')
router.register(r'musicians', MusicianView, 'musician')
router.register(r'gigs', GigView, 'gig')
router.register(r'instruments', InstrumentView, 'instrument')
router.register(r'skill_levels', SkillLevelView, 'skill_level')
router.register(r'genres', GenreView, 'genre')




urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls))
]
