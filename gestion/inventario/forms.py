from django import forms
from .models import Producto, Cliente, Usuario, EquipoInstalado, TicketSoporte


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
