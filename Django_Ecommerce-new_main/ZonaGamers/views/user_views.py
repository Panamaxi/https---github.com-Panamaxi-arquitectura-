from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
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
    return redirect('catalogo_bodeguero')

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
        messages.success(request, f'Bienvenido a Ferremas {username}')
        return redirect('/')
    else:
        messages.error(request, 'Credenciales incorrectas')
        return render_misma_vista(request)
    
def registro_bodeguero(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        name = request.POST.get('name')

        if User.objects.filter(username=username).exists():
            messages.error(request, f'El usuario {username} ya existe')
            return redirect('registro_bodeguero')

        if not all([username, password, email, name]):
            messages.error(request, 'Complete todos los campos por favor.')
            return redirect('registro_bodeguero')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.save()
        login(request, user)
        messages.success(request, f'Bienvenido a Ferremas {username}')
        return redirect('catalogo_bodeguero')

    return render(request, 'pages/registro_bodeguero.html')

def login_bodeguero(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        print(f'Intentando iniciar sesión con: {username}')  

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido de vuelta {username}')
            print('Redirigiendo a catalogo_bodeguero')  
            return redirect('catalogo_bodeguero')  
        else:
            messages.error(request, 'Credenciales incorrectas')
            print('Credenciales incorrectas')  
            
    return render(request, 'pages/login_bodeguero.html')

def login_bodeguero(request):
    logout(request)
    return redirect('catalogo_bodeguero')






    



