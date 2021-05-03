"""PredixDB URL Configuration

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
from os import name
from django.contrib import admin
from django.urls import path
from PredixDB import settings
from django.conf.urls.static import static
from PredixWeb import views

urlpatterns = [
    path("", views.showIndexPage, name='home'),
    path('admin/', admin.site.urls),
    path('login/', views.loginPage, name="login"),
    path('signup/', views.signupPage, name="signup"),
    path('about/', views.aboutPage, name="about"),
    path('movie/', views.movieinfoPage, name="movieinfo"),
    path('logout/', views.logout, name="logout"),
    path('contactus/', views.contactPage, name="contact"),
    path('addmovie/<str:mid>/', views.addMovie, name="addmovie"),
    path('addmovie/<str:mid>/<str:query>', views.addMovieFromSearch, name="addmoviesearch"),
    path('searchmovie', views.searchPage, name="searchmovie"),
]+static(settings.CODE_URL, document_root=settings.CODE_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
