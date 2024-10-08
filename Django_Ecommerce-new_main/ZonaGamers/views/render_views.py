from django.shortcuts import render, redirect
from ..models import Usuario, Carrito, Juego, CarritoJuego
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    context = {
        "user": ""
    } 
    return render(request,'pages/index.html',context)
    
def catalogo(request):
    juegos = Juego.objects.all()
    context = {
        "juegos": juegos
    }
    return render(request, 'pages/catalogo.html', context)

def producto_spider(request):
    context = []
    return render(request,'pages/producto_spider.html',context)
    

def about(request):
    context = {} 
    return render(request,'pages/about.html',context)

@login_required
def carrito(request):
    carrito = CarritoJuego.objects.filter(carrito=1)
    total = 0
    for item in carrito:
        item.total = item.juego.precio * item.cantidad
        total += item.total
    carrito.total = total
    context = {'carrito': carrito} 
    return render(request, 'pages/carrito.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    context = {} 
    return render(request,'pages/login.html',context)

def registro(request):
    context = {} 
    return render(request,'pages/registro.html',context)

def producto_spider(request):
    context = {} 
    return render(request,'pages/producto_spider.html',context)

def crud(request):
    usuarios = Usuario.objects.all()
    context = {
        "usuarios": usuarios,
    }
    return render(request, "pages/crud.html", context)

    





