from gettext import translation
import bcchapi
from django.shortcuts import redirect
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
import requests
from ..models import Carrito, CarritoJuego, Juego
from django.http import HttpResponseRedirect
from ..utils import render_misma_vista
from django.contrib import messages
from decimal import Decimal, ROUND_DOWN


def get_or_create_cart(request):
    cart, created = Carrito.objects.get_or_create(id=1)
    cart.total = sum(item.juego.precio * item.cantidad for item in cart.carritojuego_set.all())

    # Calcular total en USD usando tasa de cambio
    tasa_cambio = obtener_tasa_cambio()
    cart.total_usd = round(cart.total / tasa_cambio, 2) if tasa_cambio else None
    return cart



def add_to_cart(request, id):
    cart = get_or_create_cart(request)
    game = Juego.objects.get(id=id)
    carrito_juego, created = CarritoJuego.objects.get_or_create(carrito=cart, juego=game)
    carrito_juego.cantidad += 1
    carrito_juego.save()
    messages.success(request, f'Producto {game.nombre} agregado al carrito')
   
    return render_misma_vista(request)

def remove_from_cart(request, id):
    cart = get_or_create_cart(request)
    game = Juego.objects.get(id=id)
    carrito_juego = CarritoJuego.objects.get(carrito=cart, juego=game)
    carrito_juego.cantidad -= 1
    carrito_juego.save()
    messages.success(request, f'Producto {game.nombre} eliminado del carrito')
    return render_misma_vista(request)

def clear_cart(request):
    cart = get_or_create_cart(request)
    carrito_juego = CarritoJuego.objects.filter(carrito=cart)
    for juego in carrito_juego:
        juego.delete()
    
    messages.success(request, 'El carrito ha sido vaciado.')
    return render_misma_vista(request)


from django.urls import reverse

def convertir_usd_a_clp(monto_usd):
    tasa_cambio = obtener_tasa_cambio()
    if tasa_cambio:
        return round(monto_usd * tasa_cambio, 0) 
    else:
        return None


def iniciar_pago(request):
    cart = get_or_create_cart(request)
    
    monto_usd = cart.total_usd  # total_usd calculado previamente
    monto_clp = convertir_usd_a_clp(monto_usd)

    if not monto_clp:
        messages.error(request, "No se pudo obtener la tasa de cambio. Intente nuevamente.")
        return redirect('carrito')
    
    total_amount = cart.total  # Total del carrito
    buy_order = 'order12345'  # Orden de compra fija
    session_id = 'session12345'  # Sesión fija

    # Generar la URL del carrito usando reverse
    return_url = request.build_absolute_uri(reverse('pago_exito'))  

    transaction = Transaction(WebpayOptions(
        commerce_code=settings.TRANSBANK_COMMERCE_CODE,
        api_key=settings.TRANSBANK_API_KEY,
    ))

    try:
        response = transaction.create(
            buy_order=buy_order,
            session_id=session_id,
            
            amount=int(monto_clp),  # Transbank requiere monto como entero
            return_url=return_url  # URL generada dinámicamente
        )
        return redirect(response['url'] + '?token_ws=' + response['token'])
    except Exception as e:
        messages.error(request, f'Error al iniciar el pago: {str(e)}')
        return redirect('pago_exito')



def confirmar_pago(request):
    token = request.GET.get('token_ws')

    if not token:
        messages.error(request, 'No se recibió el token de pago.')
        return redirect('carrito')

    transaction = Transaction(WebpayOptions(
        commerce_code=settings.TRANSBANK_COMMERCE_CODE,
        api_key=settings.TRANSBANK_API_KEY,
    ))

    try:
        response = transaction.commit(token)
        if response['status'] == 'AUTHORIZED':
            messages.success(request, 'Pago realizado con éxito.')
            # Opcional: Vaciar el carrito tras el pago exitoso
            cart = get_or_create_cart(request)
            cart.carritojuego_set.all().delete()
        else:
            messages.error(request, f'Error con el pago: {response["status"]}')
    except Exception as e:
        messages.error(request, f'Error al confirmar el pago: {str(e)}')

    return redirect('carrito')  # Siempre redirige al carrito

def pago_exito(request):
    # Mensaje de éxito después del pago
    messages.success(request, "Tu pago se realizó con éxito. ¡Gracias por comprar en Ferremas!")

    return render(request, 'pages/pago_exito.html', {'request': request})

    
def convertir_dinero(request):
   
    cart = get_or_create_cart(request)
    monto_clp = cart.total

    
    tasa_cambio = obtener_tasa_cambio()

    if tasa_cambio:
        monto_usd = monto_clp / tasa_cambio
        
        messages.success(request, f"El total de ${monto_clp:,.0f} CLP es aproximadamente ${monto_usd:.2f} USD.")
    else:
        messages.error(request, "No se pudo obtener la tasa de cambio. Intente nuevamente.")

    return redirect('carrito')

def obtener_tasa_cambio():
    email = "maximilianoduarte824@gmail.com"
    contrasena = "Maxi1234"

    siete = bcchapi.Siete(email, contrasena)
    df_series = siete.buscar("dólar")

    if not df_series.empty:
        codigo_serie = df_series[df_series['spanishTitle'].str.contains("Dólar observado", case=False)].iloc[0]['seriesId']
        df_cambio = siete.cuadro(
            series=[codigo_serie],
            nombres=["usd_clp"],
            desde="2023-01-01",
            hasta="2024-12-31",
            frecuencia="D",
            observado={"usd_clp": "last"}
        )
        return df_cambio['usd_clp'].iloc[-1]
    return None









