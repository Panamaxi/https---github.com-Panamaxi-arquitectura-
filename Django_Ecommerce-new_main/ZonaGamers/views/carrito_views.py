from ..models import Carrito, CarritoJuego, Juego
from django.http import HttpResponseRedirect
from ..utils import render_misma_vista
from django.contrib import messages


def get_or_create_cart(request):
    cart, created = Carrito.objects.get_or_create(id=1)
    return cart

def add_to_cart(request, id):
    cart = get_or_create_cart(request)
    game = Juego.objects.get(id=id)
    carrito_juego, created = CarritoJuego.objects.get_or_create(carrito=cart, juego=game)
    carrito_juego.cantidad += 1
    carrito_juego.save()
    messages.success(request, f'Producto {game.nombre} agregado al carrito')
    # Redirecciona a la misma vista desde la que se hizo la petición
    return render_misma_vista(request)

def remove_from_cart(request, id):
    cart = get_or_create_cart(request)
    game = Juego.objects.get(id=id)
    carrito_juego = CarritoJuego.objects.get(carrito=cart, juego=game)
    carrito_juego.cantidad -= 1
    carrito_juego.save()
    messages.success(request, f'Producto {game.nombre} eliminado del carrito')
    return render_misma_vista(request)

def clear_cart(request,cartId):
    cart = get_or_create_cart(request)
    carrito_juego = CarritoJuego.objects.filter(carrito=cart)
    for juego in carrito_juego:
        juego.delete()
    return render_misma_vista(request)

