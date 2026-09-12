from django import forms
from .models import Producto, Cliente, Usuario, EquipoInstalado, TicketSoporte, Suministro


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_sku',
                    'nombre',
                    'marca',
                    'modelo',
                    'precio_base',
                    'meses_garantia',
                    'categoria',
                ]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['razon_social', 'numero_identificacion', 'email_contacto', 'telefono', 'direccion_fiscal', 'activo']


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'email', 'rol', 'activo']


class EquipoInstaladoForm(forms.ModelForm):
    class Meta:
        model = EquipoInstalado
        fields = ['numero_serie', 'fecha_instalacion', 'fin_garantia', 'estado', 'producto', 'cliente']
        widgets = {
            'fecha_instalacion': forms.DateInput(attrs={'type': 'date'}),
            'fin_garantia': forms.DateInput(attrs={'type': 'date'}),
        }


class TicketSoporteForm(forms.ModelForm):
    class Meta:
        model = TicketSoporte
        fields = ['codigo_ticket', 'descripcion_falla', 'prioridad', 'estado', 'equipo', 'tecnico']


# Formulario del modelo intermedio de la relación N:M (Producto <-> Proveedor).
# 'producto' no se incluye: se fija desde la vista según el producto sobre el que se opera.
class SuministroForm(forms.ModelForm):
    class Meta:
        model = Suministro
        fields = ['proveedor', 'precio_compra', 'dias_entrega_promedio', 'es_proveedor_principal']
