from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),

    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),

    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),

    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('equipos/<int:pk>/editar/', views.editar_equipo, name='editar_equipo'),
    path('equipos/<int:pk>/eliminar/', views.eliminar_equipo, name='eliminar_equipo'),

    path('tickets/', views.lista_tickets, name='lista_tickets'),
    path('tickets/<int:pk>/editar/', views.editar_ticket, name='editar_ticket'),
    path('tickets/<int:pk>/eliminar/', views.eliminar_ticket, name='eliminar_ticket'),

    path('productos/proveedores/', views.productos_proveedores, name='productos_proveedores'),
    path('categorias/<int:pk>/', views.detalle_categoria, name='detalle_categoria'),

    path('suministros/crear/<int:producto_pk>/', views.crear_suministro, name='crear_suministro'),
    path('suministros/<int:pk>/editar/', views.editar_suministro, name='editar_suministro'),
    path('suministros/<int:pk>/eliminar/', views.eliminar_suministro, name='eliminar_suministro'),
]