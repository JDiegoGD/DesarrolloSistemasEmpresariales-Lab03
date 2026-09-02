from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_sku', 'nombre', 'marca', 'modelo', 'precio_base', 'meses_garantia']