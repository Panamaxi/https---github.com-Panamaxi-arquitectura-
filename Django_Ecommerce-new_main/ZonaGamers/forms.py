from django import forms
from .models import Usuario, Producto, Pedido

from django.forms import ModelForm

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"
        
class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = "__all__"
        
# forms.py

#class ConversionForm(forms.Form):
    email = forms.EmailField(label='Email')
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    monto_usd = forms.FloatField(label='Monto en USD')

