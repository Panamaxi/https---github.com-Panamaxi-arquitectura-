from gettext import translation
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

def iniciar_pago(request):
    total_amount = 2000  
    buy_order = 'order12345'  
    session_id = 'session12345'  

   
    return_url = 'http://tu_dominio.com/confirmar_pago/'  # URL de retorno

    
    transaction = Transaction(WebpayOptions(
        commerce_code=settings.TRANSBANK_COMMERCE_CODE,
        api_key=settings.TRANSBANK_API_KEY,
        
    ))

    # Crea la transacción
    try:
        response = transaction.create(
            buy_order=buy_order,
            session_id=session_id,
            amount=total_amount,
            return_url=return_url
        )
        
        
        return redirect(response['url'] + '?token_ws=' + response['token'])
    except Exception as e:
        messages.error(request, f'Error al iniciar el pago: {str(e)}')
        return redirect('carrito')
# views.py
def confirmar_pago(request):
    token = request.GET.get('token_ws')

    transaction = Transaction(
        commerce_code=settings.TRANSBANK_COMMERCE_CODE,
        api_key=settings.TRANSBANK_API_KEY,
        
    )

    response = transaction.commit(token)

    if response['status'] == 'AUTHORIZED':
        
        messages.success(request, 'Pago realizado con éxito.')
        return redirect('carrito')  # O la vista de confirmación de pedido
    else:
        
        messages.error(request, 'Hubo un error con el pago.')
        return redirect('carrito')


#def create(request):
    if request.method == 'POST':
        # Generar buy_order y session_id
        buy_order = str(uuid.uuid4())  # ID único para la orden de compra
        session_id = request.session.session_key or str(uuid.uuid4())  # ID de sesión

        # Parámetros enviados desde el formulario
        amount = request.POST.get('amount')  # Monto
        card_number = request.POST.get('card_number')
        cvv = request.POST.get('cvv')
        card_expiration_date = request.POST.get('card_expiration_date')

        # URL y headers para la API
        url = f"{settings.TRANSBANK_API_URL}/rswebpaytransaction/api/webpay/v1.3/transactions"
        headers = {
            "Tbk-Api-Key-Id": settings.TRANSBANK_COMMERCE_CODE,
            "Tbk-Api-Key-Secret": settings.TRANSBANK_API_KEY,
            "Content-Type": "application/json"
        }

        
        
        
        buy_order = '1a2b3c4d-1234-5678-9101-11213141abcd'
        
        session_id = 'x1y2z3a4b5c6d7e8f9g0'
        amount = 1000.0  # Para pruebas, monto de 1000 pesos.
        card_number = '4051 8856 0044 6623'
        cvv = '123'
        card_expiration_date = '12/25'
        
        data = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": float(amount),
            "card_number": card_number,
            "cvv": cvv,
            "card_expiration_date": card_expiration_date
        }

        
        response = requests.post(url, headers=headers, json=data)

        
        if response.status_code == 200:
            response_data = response.json()
            #return render(request, 'pages/confirmacion_pago.html', {'response': response_data})
        else:
            return render(request, 'pages/confirmacion_pago.html', {'error': response.json()})

    return render(request, 'pages/create.html')





