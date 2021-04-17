"""invest URL Configuration

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
from django.urls import path
from app import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^auth/registration', views.registration, name='registration'),
    url(r'^auth/login', views.login, name='login'),
    url(r'^profile/logout', views.logout, name='logout'),
    url(r'^invest_item', views.get_invest_item, name='invest_item'),
    url(r'^team_item', views.get_team_item, name = 'team_item'),
    url(r'^change_profile', views.change_profile, name='change_profile'),
    url(r'^get_profile', views.get_profile, name='get_profile'),
    url(r'^main_invest', views.main_invest, name='main_invest'),
    url(r'^main_team', views.main_team, name='main_team'),
]
