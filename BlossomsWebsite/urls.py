"""BlossomsWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from homepage import views as homepage_views
from about import views as about_us_views
from teams import views as teams_views
from events import views as events_views
from store import views as store_views
from account import views as account_views

urlpatterns = [
    path('secret/', admin.site.urls),
    path('', homepage_views.home, name='home'),
    path('about/', about_us_views.about, name='about'),
    path('teams/', teams_views.teams, name='teams'),
    path('events/', events_views.events, name='events'),
    path('store/', store_views.store, name='store'),
    path('login/', include('django.contrib.auth.urls')),
    path('login/', account_views.login_user, name='login'),
    path('logout_user', account_views.logout_user, name='logout'),
    path('register/', account_views.register_user, name='register'),
    path('manage/', account_views.manage, name='manage'),
    path('manage/add_athlete/', account_views.add_athlete, name='add-athlete'),
    path('manage/team_registration/', account_views.team_registration, name='team-registration'),
    path('athlete_csv', account_views.athlete_csv, name='athlete-csv')
]
