from django.urls import path
from . import views
urlpatterns = [
    path('', views.redirect_, name = "redirect"),
    path('login/', views.login, name = "login"),
    path('register/', views.register, name = "register"),
    path('cloud/', views.cloud, name = "cloud"),
]