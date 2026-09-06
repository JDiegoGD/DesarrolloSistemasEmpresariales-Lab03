# DesarrolloSistemasEmpresariales-Lab03

## Problematica:
##### Gestión ineficiente en la cadena de suministro y servicios postventa de una Empresa Distribuidora de Equipos Médicos.


## Usuarios Involucrados:
* Administrador del Sistema: Gestiona permisos, roles y configuraciones.
* Jefe de Inventario y Logística: Registra la entrada de lotes, control de existencias, ubicaciones en almacén y despachos.
* Asesor Comercial: Genera cotizaciones, registra clientes y formaliza las órdenes de venta.
* Técnico de Soporte: Registra los mantenimientos, diagnósticos y solicitudes de repuestos para los equipos instalados.
* Cliente: Accede a un portal para solicitar soporte, revisar el estado de los equipos y consultar facturas.

## Requisitos Funcionales del Sistema Web:
* **RF-01** Crear Producto en Catálogo - Crear: Permitir al Jefe de Inventario registrar nuevos equipos médicos, especificando datos obligatorios como SKU, nombre, marca, modelo y costo base.
* **RF-02** Registrar Cliente - Crear: El sistema debe permitir al Asesor Comercial registrar nuevos clientes (clínicas u hospitales), ingresando su RUC/NIT, razón social, dirección fiscal y datos de contacto.
* **RF-03** Apertura de Ticket de Soporte - Crear: El sistema debe permitir al Cliente o Técnico crear un ticket de incidencia técnica vinculando el número de serie del equipo afectado y detallando la falla reportada.
* **RF-04** Listar Equipos Instalados - Leer: El sistema debe permitir a los usuarios autorizados consultar un listado general de los equipos en servicio, incluyendo filtros por cliente, estado de garantía y rango de fechas.
* **RF-05** Consultar Panel de Tickets - Leer: Permitir al Técnico y al Cliente visualizar el estado de las solicitudes de mantenimiento activas, filtradas por prioridad o estado.
* **RF-06** Actualizar Datos del Cliente - Actualizar: Permitir al Administrador o Asesor Comercial modificar la información de contacto y ubicación de un cliente registrado.
* **RF-07** Actualizar Estado de Ticket - Actualizar: Permitir al Técnico de Soporte actualizar el estado del ticket, asignar diagnósticos y registrar repuestos utilizados.
* **RF-08** Inactivar Usuario o Registro - Eliminar: El sistema debe permitir al Administrador realizar la baja lógica (desactivación) de usuarios o clientes inactivos para impedir su acceso al sistema sin perder el historial operativo.

## Cobertura de Operaciones CRUD
* Crear (Create): RF-01, RF-02, RF-03
* Leer / Listar (Read): RF-04, RF-05
* Actualizar (Update): RF-06, RF-07
* Eliminar / Inactivar (Delete): RF-08

---


```python
class Cliente(models.Model):
    razon_social = models.CharField(max_length=150)
    numero_identificacion = models.CharField(max_length=20, unique=True)
    email_contacto = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion_fiscal = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.razon_social


class Producto(models.Model):
    codigo_sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    meses_garantia = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} - {self.modelo}"


class Usuario(models.Model):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('VENTAS', 'Asesor Comercial'),
        ('LOGISTICA', 'Jefe de Inventario'),
        ('TECNICO', 'Técnico de Soporte'),
    ]
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROLES)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_completo} ({self.rol})"


class EquipoInstalado(models.Model):
    ESTADOS = [
        ('OPERATIVO', 'Operativo'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('INACTIVO', 'Inactivo'),
    ]
    numero_serie = models.CharField(max_length=100, unique=True)
    fecha_instalacion = models.DateField()
    fin_garantia = models.DateField()
    estado = models.CharField(max_length=30, choices=ESTADOS, default='OPERATIVO')
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='equipos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='equipos')

    def __str__(self):
        return f"Serie: {self.numero_serie} - {self.cliente.razon_social}"


class TicketSoporte(models.Model):
    PRIORIDADES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]
    ESTADOS = [
        ('ABIERTO', 'Abierto'),
        ('EN_PROCESO', 'En Proceso'),
        ('RESUELTO', 'Resuelto'),
        ('CERRADO', 'Cerrado'),
    ]
    codigo_ticket = models.CharField(max_length=20, unique=True)
    descripcion_falla = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='MEDIA')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ABIERTO')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    equipo = models.ForeignKey(EquipoInstalado, on_delete=models.CASCADE, related_name='tickets')
    tecnico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados')

    def __str__(self):
        return f"{self.codigo_ticket} - {self.estado}"
```

## Representacion de Relaciones
* Entidades Independientes:
    * Clientes
    * Productos
    * Usuarios
    * Entidades Vinculadas (Relación 1:N):
    * Plaintext

* Entidad A: Clientes
* Entidad B: Productos
* Entidad C: Usuarios


### Explicación de la Relación:
* Un Cliente (Entidad D) puede poseer N Equipos_Instalados (Entidad E).
* Un Equipo_Instalado (Entidad E) pertenece obligatoriamente a 1 Cliente (Entidad D).


## Implementar READ
```
templates/
└── inventario/
    ├── base.html
    ├── crear_producto.html
    ├── lista_clientes.html
    ├── lista_equipos.html
    ├── lista_productos.html
    ├── lista_tickets.html
    └── lista_usuarios.html
```

## Implementar UPDATE
```
templates/
└── inventario/
    ├── base.html
    ├── crear_producto.html
    ├── editar_cliente.html
    ├── editar_equipo.html
    ├── editar_producto.html
    ├── editar_ticket.html
    ├── editar_usuario.html
    ├── lista_clientes.html
    ├── lista_equipos.html
    ├── lista_productos.html
    ├── lista_tickets.html
    └── lista_usuarios.html
```

