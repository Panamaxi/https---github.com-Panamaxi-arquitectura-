from django.db import models

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