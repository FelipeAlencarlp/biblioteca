from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Livros, Categoria, Emprestimos
from .forms import CadastroLivro, CategoriaLivro

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario']).id
        status_categoria = request.GET.get('cadastro_categoria')
        status_emprestimo = request.GET.get('cadastro_emprestimo')
        livros = Livros.objects.filter(usuario = usuario)
        form = CadastroLivro()
        form_categoria = CategoriaLivro()

        usuarios = Usuario.objects.all()
        livros_emprestar = Livros.objects.filter(usuario = usuario).filter(emprestado = False)

        # relaciona os campos com o usuário que está logado
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)

        return render(request, 'home.html', {'livros': livros,
                                             'usuario_logado': request.session.get('usuario'),
                                             'form': form,
                                             'form_categoria': form_categoria,
                                             'status_categoria': status_categoria,
                                             'status_emprestimo': status_emprestimo,
                                             'usuarios': usuarios,
                                             'livros_emprestar': livros_emprestar})

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

            usuarios = Usuario.objects.all()
            livros = Livros.objects.filter(usuario_id = request.session.get('usuario'))
            livros_emprestar = Livros.objects.filter(usuario = usuario).filter(emprestado = False)

            # relaciona os campos com o usuário que está logado
            form.fields['usuario'].initial = request.session['usuario']
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario)

            return render(request, 'ver_livro.html', {'livro': livro,
                                                      'categoria_livro': categoria_livro,'emprestimos': emprestimos,
                                                      'usuario_logado': request.session.get('usuario'),
                                                      'form': form,
                                                      'slug_livro': slug,
                                                      'form_categoria': form_categoria,
                                                      'usuarios': usuarios,
                                                      'livros': livros,
                                                      'livros_emprestar': livros_emprestar})
        
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
        nome_emprestado = request.POST.get('nome_emprestado')
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')
        livro_emprestado = request.POST.get('livro_emprestado')

        if nome_emprestado_anonimo:
            emprestimo = Emprestimos(nome_emprestado_anonimo = nome_emprestado_anonimo,
                                 livro_id = livro_emprestado)
            
        else:
            emprestimo = Emprestimos(nome_emprestado_id = nome_emprestado,
                                     livro_id = livro_emprestado)

        emprestimo.save()

        livro = Livros.objects.get(id = livro_emprestado)
        livro.emprestado = True
        livro.save()

        return redirect('/livro/home/?cadastro_emprestimo=1')
    
    return HttpResponse('Impossível cadastrar!')


def excluir_livro(request, slug):
    livro = Livros.objects.get(slug = slug).delete()

    return redirect('/livro/home/')
