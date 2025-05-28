from rest_framework import serializers
from .models import Producto, Precio

class PrecioSerializer(serializers.ModelSerializer):
    fecha = serializers.DateTimeField(format="%d/%m/%Y", help_text="Fecha del precio en formato DD/MM/YYYY.")
    
    class Meta:
        model = Precio
        fields = ['fecha', 'valor']


class ProductoSerializer(serializers.ModelSerializer):
    precios = PrecioSerializer(source='precios', many=True, read_only=True)

    codigo_del_producto = serializers.CharField(source='codigo_producto', help_text="Código identificador del producto.", read_only=False)
    codigo = serializers.CharField(source='codigo_interno', help_text="Código interno de referencia.")
    marca = serializers.CharField(help_text="Marca del producto.")
    nombre = serializers.CharField(help_text="Nombre del producto.")

    class Meta:
        model = Producto
        fields = [
            'codigo_del_producto',
            'marca',
            'codigo',
            'nombre',
            'precios'
        ]

    def create(self, validated_data):
        producto = Producto.objects.create(**validated_data)
        Precio.objects.create(producto=producto)
        return producto

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)