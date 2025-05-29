from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username

class Producto(models.Model):
    codigo_producto = models.CharField(max_length=50, unique=True, primary_key=True, verbose_name="Código del Producto")
    marca = models.CharField(max_length=100)
    codigo_interno = models.CharField(max_length=50, unique=True, verbose_name="Código Interno")
    nombre = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} ({self.codigo_producto})"

class Precio(models.Model):
    producto = models.ForeignKey(Producto, to_field='codigo_producto', related_name='precios', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    valor = models.IntegerField(default=999999999) # Valor por defecto de 999999999 CLP

    class Meta:
        verbose_name = "Precio"
        verbose_name_plural = "Precios"
        ordering = ['-fecha']

    def __str__(self):
        return f"Precio de {self.producto.nombre} - ${self.valor} CLP en {self.fecha.strftime('%Y-%m-%d %H:%M')}"
    
class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='activo')

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Carrito Item"
        verbose_name_plural = "Carrito Items"
        unique_together = ('carrito', 'producto')

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    def subtotal(self):
        precio_actual = self.producto.precios.first().valor if self.producto.precios.exists() else 999999999
        return self.cantidad * precio_actual