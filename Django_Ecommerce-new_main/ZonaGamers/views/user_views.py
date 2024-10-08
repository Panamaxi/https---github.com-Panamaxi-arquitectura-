from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from ..utils import render_misma_vista
from django.contrib.auth.models import User

def login_user(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if username is None or password is None:
        messages.error(request, 'Ha ocurrido un error al iniciar sesión')
        return render_misma_vista(request)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, f'Bienvenido de vuelta {username}')
        return redirect('/')
    else:
        messages.error(request, 'Credenciales incorrectas')
        return render_misma_vista(request)
    
def logout_user(request):
    logout(request)
    return render_misma_vista(request)

def register_user(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    email = request.POST.get('email', None)
    name = request.POST.get('name', None)
    if User.objects.filter(username=username).exists():
        messages.error(request, f'El usuario {username} ya existe')
        return redirect('login')
    if username is None or password is None or email is None or name is None:
        messages.error(request, 'Complete todos los campos por favor.')
        return render_misma_vista(request)  
    user = User.objects.create_user(username, email, password)
    if user is not None:
        user.first_name = name
        user.save()
        login(request, user)
        messages.success(request, f'Bienvenido a ZonaGamers {username}')
        return redirect('/')
    else:
        messages.error(request, 'Credenciales incorrectas')
        return render_misma_vista(request)
