from django.contrib import admin
from django.urls import path
from author import views

app_name= "author"

urlpatterns = [
    path("login", views.login, name="author.login"),
    path("logout", views.logout, name="author.logout"),
    path("register", views.register, name="author.register"),
    path("profile", views.profile, name="author.profile"),
    path("", views.profile, name="author.empty"),
]
