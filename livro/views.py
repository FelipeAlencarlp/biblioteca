from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Livros, Categoria, Emprestimos
from .forms import CadastroLivro, CategoriaLivro, EmprestimoLivro

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario']).id
        status_categoria = request.GET.get('cadastro_categoria')
        status_emprestimo = request.GET.get('cadastro_emprestimo')
        livros = Livros.objects.filter(usuario = usuario)
        form = CadastroLivro()
        form_categoria = CategoriaLivro()
        form_emprestimo = EmprestimoLivro()

        # relaciona os campos com o usuário que está logado
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)

        return render(request, 'home.html', {'livros': livros,
                                             'usuario_logado': request.session.get('usuario'),
                                             'form': form,
                                             'form_categoria': form_categoria,
                                             'form_emprestimo': form_emprestimo,
                                             'status_categoria': status_categoria,
                                             'status_emprestimo': status_emprestimo})

    return redirect('/auth/login/?status=2')


def ver_livro(request, slug):
    if request.session.get('usuario'):
        livro = Livros.objects.get(slug = slug)

        if request.session.get('usuario') == livro.usuario.id:
            usuario = Usuario.objects.get(id = request.session['usuario']).id
            categoria_livro = Categoria.objects.filter(usuario = request.session.get('usuario'))
            emprestimos = Emprestimos.objects.filter(livro = livro)
            form = CadastroLivro()
            form_categoria = CategoriaLivro()
            form_emprestimo = EmprestimoLivro()

            # relaciona os campos com o usuário que está logado
            form.fields['usuario'].initial = request.session['usuario']
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)

            return render(request, 'ver_livro.html', {'livro': livro,
                                                      'categoria_livro': categoria_livro,'emprestimos': emprestimos,
                                                      'usuario_logado': request.session.get('usuario'),
                                                      'form': form,
                                                      'slug_livro': slug,
                                                      'form_categoria': form_categoria,
                                                      'form_emprestimo': form_emprestimo})
        
        return HttpResponse('Esse livro não é seu')
    
    return redirect('/auth/login/?status=2')


def cadastrar_livro(request):
    if request.method == "POST":
        form = CadastroLivro(request.POST)
        
        if form.is_valid:
            form.save()

            return redirect('/livro/home/')
        
        return HttpResponse('Dados inválidos!')


def cadastrar_categoria(request):
    form = CategoriaLivro(request.POST)
    nome = form.data['nome']
    descricao = form.data['descricao']
    id_usuario = request.POST.get('usuario')

    if int(id_usuario) == int(request.session.get('usuario')):
        # user = Usuario.objects.get(id = id_usuario)  instância de usuário
        categoria = Categoria(nome = nome,
                              descricao = descricao,
                              usuario_id = id_usuario)
        categoria.save()

        return redirect('/livro/home/?cadastro_categoria=1')

    return HttpResponse('Impossível cadastrar!')


def cadastrar_emprestimo(request):
    if request.method == "POST":
        form = EmprestimoLivro(request.POST)
        
        if form.is_valid:
            form.save()

            return redirect('/livro/home/?cadastro_emprestimo=1')
        
        return HttpResponse('Dados inválidos!')


def excluir_livro(request, slug):
    livro = Livros.objects.get(slug = slug).delete()

    return redirect('/livro/home/')
