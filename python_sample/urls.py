from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="main-page"),
    path('nasswallet-paymet-gateway/login', views.login, name="login")
]