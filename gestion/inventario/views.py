from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm

# Vista para Listar Productos (Destino del redirect)
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

# Vista para Crear un Producto (CREATE mediante ORM)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda en SQLite usando Django ORM
            return redirect('lista_productos')  # Redirige al listado
    else:
        form = ProductoForm()
    
    return render(request, 'inventario/crear_producto.html', {'form': form})