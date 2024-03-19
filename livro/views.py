from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Livros, Categoria, Emprestimos

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario']).id
        livros = Livros.objects.filter(usuario = usuario)

        return render(request, 'home.html', {'livros': livros})

    return redirect('/auth/login/?status=2')


def ver_livro(request, slug):
    if request.session.get('usuario'):
        livro = Livros.objects.get(slug = slug)

        if request.session.get('usuario') == livro.usuario.id:
            categoria_livro = Categoria.objects.filter(usuario_id = request.session.get('usuario'))
            emprestimos = Emprestimos.objects.filter(livro = livro)

            return render(request, 'ver_livro.html', {'livro': livro, 'categoria_livro': categoria_livro, 'emprestimos': emprestimos})
        
        return HttpResponse('Esse livro não é seu')
    
    return redirect('/auth/login/?status=2')
