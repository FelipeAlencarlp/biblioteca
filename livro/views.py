from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Livros, Categoria, Emprestimos
from .forms import CadastroLivro

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario']).id
        livros = Livros.objects.filter(usuario = usuario)
        form = CadastroLivro()

        return render(request, 'home.html', {'livros': livros,
                                             'usuario_logado': request.session.get('usuario'),
                                             'form': form})

    return redirect('/auth/login/?status=2')


def ver_livro(request, slug):
    if request.session.get('usuario'):
        livro = Livros.objects.get(slug = slug)

        if request.session.get('usuario') == livro.usuario.id:
            categoria_livro = Categoria.objects.filter(usuario = request.session.get('usuario'))
            emprestimos = Emprestimos.objects.filter(livro = livro)
            form = CadastroLivro()

            return render(request, 'ver_livro.html', {'livro': livro,
                                                      'categoria_livro': categoria_livro,'emprestimos': emprestimos,
                                                      'usuario_logado': request.session.get('usuario'),
                                                      'form': form})
        
        return HttpResponse('Esse livro não é seu')
    
    return redirect('/auth/login/?status=2')


def cadastrar_livro(request):
    if request.method == "POST":
        form = CadastroLivro(request.POST)
        
        if form.is_valid:
            form.save()

            return HttpResponse('Livro salvo com sucesso.')
        else:
            return HttpResponse('Dados inválidos!')
