from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Livros

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario']).id
        livros = Livros.objects.filter(usuario = usuario)

        return render(request, 'home.html', {'livros': livros})

    return redirect('/auth/login/?status=2')


def ver_livro(request, slug):
    livro = Livros.objects.get(slug = slug)

    return render(request, 'ver_livro.html', {'livro': livro})
