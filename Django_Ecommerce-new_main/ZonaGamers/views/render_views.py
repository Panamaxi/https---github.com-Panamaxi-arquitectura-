from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from ..models import Usuario, Carrito, Juego, CarritoJuego
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    context = {
        "user": ""
    } 
    return render(request,'pages/index.html',context)
    
def catalogo(request):
    query = request.GET.get('q')
    
    if query:
        # Filtramos los juegos que contienen el término de búsqueda en el nombre
        juegos = Juego.objects.filter(nombre__icontains=query)
    else:
        # Si no hay búsqueda, mostramos todos los juegos
        juegos = Juego.objects.all()

    context = {
        "juegos": juegos,
        "mensaje_error": None,  # Inicializamos el mensaje de error como None
    }

    # Si no se encuentran juegos después de la búsqueda, asignamos un mensaje de error
    if query and not juegos.exists():
        context["mensaje_error"] = "No se encontraron los productos en el catalogo de ferremas."

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

def bodeguero(request):
    context = {} 
    return render(request,'pages/bodeguero.html',context)

def catalogo_bodeguero(request):
    juegos = Juego.objects.all() 
    # Obtiene todos los productos
    return render(request, 'pages/catalogo_bodeguero.html', {'juegos': juegos})

def detalle_producto(request, id):
    juego = get_object_or_404(Juego, id=id)
    return render(request, 'pages/detalle_producto.html', {'juego': juego})

def aumentar_stock(request, id):
    juego = get_object_or_404(Juego, id=id)
    juego.stock += 1  # Aumentar el stock en 1
    juego.save()
    messages.success(request, f'Se ha aumentado el stock del juego {juego.nombre}.')
    return redirect(request, 'pages/catalogo_bodeguero.html')

def disminuir_stock(request, id):
    juego = get_object_or_404(Juego, id=id)
    if juego.stock > 0:
        juego.stock -= 1  # Disminuir el stock en 1
        juego.save()
        messages.success(request, f'Se ha disminuido el stock del juego {juego.nombre}.')
    else:
        messages.error(request, f'No se puede disminuir el stock del juego {juego.nombre}. Stock ya es 0.')
    return redirect(request, 'pages/catalogo_bodeguero.html')


    





