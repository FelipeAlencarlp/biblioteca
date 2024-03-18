from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('ver_livro/<slug:slug>', views.ver_livro, name='ver_livro'),
]