from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
from hashlib import sha256 # lib para hash de password

def login(request):
    if request.session.get('usuario'):
        return redirect('/livro/home/')
    
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})


def cadastro(request):
    if request.session.get('usuario'):
        return redirect('/livro/home/')
    
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})


def valida_cadastro(request):
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    confirma_senha = request.POST.get('senha')

    usuario = Usuario.objects.filter(email = email)

    if len(nome.strip()) == 0 or len(senha.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')

    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')

    if len(usuario) > 0:
        return redirect('/auth/cadastro/?status=3')
    
    try:
        senha = sha256(senha.encode()).hexdigest() # converte em hexadecimal de 64 caracteres
        usuario = Usuario(
            nome = nome,
            email = email,
            senha = senha,
        )
        usuario.save()

        return redirect('/auth/cadastro/?status=0')
    except:
        return redirect('/auth/cadastro/?status=4')


def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email = email).filter(senha = senha)

    if len(usuario) == 0:
        return redirect('/auth/login/?status=1')
    
    elif len(usuario) > 0:
        request.session['usuario'] = usuario[0].id

        return redirect('/livro/home/')


def logout(request):
    request.session.flush()

    return redirect('/auth/login/')