from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.urls import reverse

from apiferremas.models import Carrito, CarritoItem, Producto

import bcchapi
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions


# --- Lógica auxiliar --- #

def render_misma_vista(request):
    """
    Renderiza la misma vista que se está solicitando, útil para mantener el contexto del carrito.
    """
    return render(request, request.path.split('/')[-1], {})

def obtener_tasa_cambio():
    siete = bcchapi.Siete("maximilianoduarte824@gmail.com", "Maxi1234")
    df_series = siete.buscar("dólar")
    if not df_series.empty:
        codigo = df_series[df_series['spanishTitle'].str.contains("observado", case=False)].iloc[0]['seriesId']
        df_cambio = siete.cuadro(
            series=[codigo],
            nombres=["usd_clp"],
            desde="2023-01-01",
            hasta="2024-12-31",
            frecuencia="D",
            observado={"usd_clp": "last"}
        )
        return df_cambio['usd_clp'].iloc[-1]
    return None


def convertir_usd_a_clp(monto_usd):
    tasa = obtener_tasa_cambio()
    return round(monto_usd * tasa, 0) if tasa else None


# --- Carrito --- #

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Carrito.objects.get_or_create(usuario=request.user)
        # Calculamos el total usando el método definido en el modelo
        cart_total = cart.total()
        tasa = obtener_tasa_cambio()
        total_usd = round(cart_total / tasa, 2) if tasa else None
        # Si quieres guardar estos valores en el modelo, deberías tener campos para ello, si no, simplemente devuelve o usa estas variables
        cart.total_calculado = cart_total
        cart.total_usd_calculado = total_usd
        return cart
    else:
        return None  # usuario anónimo no tiene carrito persistente


def add_to_cart(request, codigo_producto):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para agregar productos al carrito.")
        return redirect("login")

    cart = get_or_create_cart(request)
    producto = get_object_or_404(Producto, codigo_producto=codigo_producto)

    carrito_item, created = CarritoItem.objects.get_or_create(carrito=cart, producto=producto)
    carrito_item.cantidad += 1
    carrito_item.save()
    messages.success(request, f'Producto {producto.nombre} agregado al carrito')
    return render_misma_vista(request)


def remove_from_cart(request, codigo_producto):
    cart = get_or_create_cart(request)
    producto = get_object_or_404(Producto, codigo_producto=codigo_producto)
    carrito_item = get_object_or_404(CarritoItem, carrito=cart, producto=producto)

    carrito_item.cantidad -= 1
    if carrito_item.cantidad <= 0:
        carrito_item.delete()
    else:
        carrito_item.save()

    messages.success(request, f'{producto.nombre} eliminado del carrito')
    return render_misma_vista(request)


def clear_cart(request):
    cart = get_or_create_cart(request)
    if cart:
        cart.items.all().delete()
        messages.success(request, 'El carrito ha sido vaciado.')
    return render_misma_vista(request)


# --- Pago --- #

def iniciar_pago(request):
    cart = get_or_create_cart(request)

    if not cart or cart.total() == 0:
        messages.error(request, "Tu carrito está vacío.")
        return redirect('carrito')

    monto_clp = convertir_usd_a_clp(cart.total_usado_calculado if hasattr(cart, 'total_usado_calculado') else 0)
    if not monto_clp:
        messages.error(request, "No se pudo obtener la tasa de cambio.")
        return redirect('carrito')

    return_url = request.build_absolute_uri(reverse('pago_exito'))

    transaction = Transaction(WebpayOptions(
        commerce_code=settings.TRANSBANK_COMMERCE_CODE,
        api_key=settings.TRANSBANK_API_KEY,
    ))

    try:
        response = transaction.create(
            buy_order=str(cart.id),
            session_id=str(request.user.id),
            amount=int(monto_clp),
            return_url=return_url
        )
        return redirect(response['url'] + '?token_ws=' + response['token'])
    except Exception as e:
        messages.error(request, f'Error al iniciar el pago: {str(e)}')
        return redirect('carrito')


def confirmar_pago(request):
    token = request.GET.get('token_ws')
    if not token:
        messages.error(request, 'No se recibió token de pago.')
        return redirect('carrito')

    transaction = Transaction(WebpayOptions(
        commerce_code=settings.TRANSBANK_COMMERCE_CODE,
        api_key=settings.TRANSBANK_API_KEY,
    ))

    try:
        response = transaction.commit(token)
        if response['status'] == 'AUTHORIZED':
            messages.success(request, 'Pago realizado con éxito.')
            cart = get_or_create_cart(request)
            if cart:
                cart.items.all().delete()
        else:
            messages.error(request, f'Error con el pago: {response["status"]}')
    except Exception as e:
        messages.error(request, f'Error al confirmar el pago: {str(e)}')

    return redirect('carrito')


def pago_exito(request):
    messages.success(request, "Tu pago se realizó con éxito. ¡Gracias por tu compra!")
    return render(request, 'pages/pago_exito.html')


def convertir_dinero(request):
    cart = get_or_create_cart(request)
    if not cart:
        messages.error(request, "No tienes carrito.")
        return redirect('carrito')

    monto_clp = cart.total()
    tasa = obtener_tasa_cambio()

    if tasa:
        monto_usd = monto_clp / tasa
        messages.success(request, f"CLP ${monto_clp:,.0f} ≈ USD ${monto_usd:.2f}")
    else:
        messages.error(request, "No se pudo obtener la tasa de cambio.")

    return redirect('carrito')
