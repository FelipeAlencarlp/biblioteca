from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('ver_livro/<slug:slug>', views.ver_livro, name='ver_livro'),
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('cadastrar_categoria/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('cadastrar_emprestimo/', views.cadastrar_emprestimo, name='cadastrar_emprestimo'),
    path('devolver_livro/', views.devolver_livro, name='devolver_livro'),
    path('alterar_livro/', views.alterar_livro, name='alterar_livro'),
    path('peguei_emprestado/', views.peguei_emprestado, name='peguei_emprestado'),
    path('excluir_livro/<slug:slug>', views.excluir_livro, name='excluir_livro'),
]