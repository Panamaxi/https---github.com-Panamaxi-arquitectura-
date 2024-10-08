from django.contrib import admin
from .models import Usuario, Juego, Pedido, Carrito,CarritoJuego


admin.site.register(Usuario)
admin.site.register(Juego)
admin.site.register(Pedido)
admin.site.register(Carrito)
admin.site.register(CarritoJuego)


# Register your models here.
