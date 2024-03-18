from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario

def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario']).nome
        return HttpResponse(f'Ola {usuario}')

    return redirect('/auth/login/?status=2')
