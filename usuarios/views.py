from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        
        try:
            usuario = User.objects.get(username=username)
            return HttpResponse('Já existe um usuário cadastrado')
        except User.DoesNotExist:
            usuario = User.objects.create_user(username=username, password=senha)
            usuario.save() 
            return HttpResponse(f'Usuário {usuario.username} cadastrado com sucesso!')

      
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        
        user = authenticate(username=username, password=senha)
    
        if user:
            login(request, User)
            return redirect ('/salas')
        else:
            return HttpResponse('Usuário ou senha inválidos!')
    

def sair(request):
    logout(request) 
    return redirect('/usuarios/logar')

def trocar(request):
    if request.method =="GET":
       return render(request, "trocarsenha.html")

