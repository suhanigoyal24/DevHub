from django.urls import path
from . import views
from devhub_app import views

urlpatterns = [
    path("", views.home, name="home"),  # /api/
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path('', views.home),  # Home at /
]
