"""ticketswatcher URL Configuration

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
from django.urls import path
from . import views, management_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('concert/<int:concert_id>', views.concert, name='concert'),
    path('concert/<int:concert_id>/watch', views.watch, name='watch'),
    path('watchers', views.watchers, name='watchers'),

    path('loadConcerts', views.loadConcerts, name='loadConcerts'),
    path('loadTickets/<int:concert_id>', views.loadTickets, name='loadTickets'),
    path('checkWatchers', views.checkWatchers, name='checkWatchers'),
    path('sendTestEmail', views.sendTestEmail, name='sendTestEmail'),
    path('deleteWatcher/<str:uuid>', views.deleteWatcher, name='deleteWatcher')
]

urlpatterns += management_urls.urlpatterns
